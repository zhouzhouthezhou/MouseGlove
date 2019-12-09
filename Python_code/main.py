import IMUclass
import softwareUart
import time
import machine

def run():
	print("RUN: main.py")
	#imu = IMUclass.IMU()
	#imu.orientation()
	#sam = softwareUart.UartCom()
	pin = machine.Pin(12, machine.Pin.OUT)
	print("hejfdsalk")
	while(True):
		pin.value(1)
		#sam.send_Message("I AM SAM")
		time.sleep(2)
		pin.value(0)


if __name__ == '__main__':
	run()
