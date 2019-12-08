import IMUclass

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	imu.config()
	while(True):
		imu.test()

if __name__ == '__main__':
	run()
