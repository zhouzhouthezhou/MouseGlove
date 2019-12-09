import softwareUart
#import IMUclass
import time
from machine import Pin

def run():
	print("RUN: main.py")
	#imu = IMUclass.IMU()
	#imu.orientation()
	sam = softwareUart.UartCom()
	mes = "I am sam"
	buf = [elem.encode("hex") for elem in mes]
	while(True):
		sam.send_Message()
		time.sleep(2)



if __name__ == '__main__':
	run()
