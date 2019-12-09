import IMUclass
import time
from machine import Pin

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	imu.orientation()


if __name__ == '__main__':
	run()
