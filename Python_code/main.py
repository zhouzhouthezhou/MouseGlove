import IMUclass
import time
from machine import Pin

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	print("fdsafds")
	imu.orientation()
	imu.read_click()


if __name__ == '__main__':
	run()
