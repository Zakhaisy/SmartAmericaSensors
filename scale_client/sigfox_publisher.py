##1. install python serial package, details can be found at http://pyserial.sourceforge.net/pyserial.html#installation
##2. change the permission of your device, using "chmod o+rw". In my machine, it is "sudo chmod o+rw /dev/ttyUSB0"


from publisher import Publisher
from sensed_event import SensedEvent
import time
import serial 

class SigfoxPublisher(Publisher):
	def __init__(self, topic_prefix, topic_suffix = ""):
		self._topic_prefix = topic_prefix
		self._topic_suffix = topic_suffix
		self._ser=None

	def _ex_handler(self,obj):
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(obj).__name__, obj.args)
            print message

	def connect(self,
                _port='/dev/ttyUSB0',
                _baudrate=9600,
                _parity=serial.PARITY_NONE,
                _stopbits=serial.STOPBITS_ONE,
                _bytesize=serial.EIGHTBITS):
		try:
                            
                    self._ser=serial.Serial(
                    port=_port,
                    baudrate=_baudrate,
                    parity=_parity,
                    stopbits=_stopbits,
                    bytesize=_bytesize)
                    
                except Exception as err: 
                    self._ex_handler(err)
                    return False
		if(not self._ser.isOpen()):
                    self._ser.open()
		return True

	def send(self, event):
		# Make message from a sensed event
		topic = self._topic_prefix + "/" + event.sensor + "/" + self._topic_suffix
		msg = event.msg + " @" + str(event.timestamp)

		# Publish message "||" can be redefined. but '\r\n' is mandatory
		try:
                    #self._ser.write(topic+"||"+msg+'\r\n')
                    #use the above paras to send actual sensor data    
                    self._ser.write("AT$SS=0123456789abcdef"+'\r\n')
                except Exception as err: 
                    self._ex_handler(err)
                    return False
                
		print "SigFox message published to " + topic
		return True
	def receive(self):
                #read message from the sigfox adapter
                ret='' #return message read
                while self._ser.inWaiting()>0:
                    ret+=self._ser.read(1)
                return ret
                    
def main():
        sig=SigfoxPublisher("pre","suf")

        if(sig.connect()):
            event=SensedEvent("SampleSensor", "SampleMSG", 1)
            sig.send(event)#convert event to sigfox format here!
            time.sleep(1)
            print(sig.receive())
        else:
            exit
        


if __name__ == "__main__":
    main()         