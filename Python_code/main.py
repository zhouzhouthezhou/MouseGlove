import IMUclass

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	while(True):
		imu.test()

if __name__ == '__main__':
	run()
