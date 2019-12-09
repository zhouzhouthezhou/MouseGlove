import IMUclass
import softwareUart
import time
from machine import Pin

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	#imu.orientation()
	sam = softwareUart.UartCom()
	while(True):
		sam.send_Message("I AM SAM")
		time.sleep(2)



if __name__ == '__main__':
	run()
