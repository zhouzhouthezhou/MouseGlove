import IMUclass

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	imu.orientation()

if __name__ == '__main__':
	run()
