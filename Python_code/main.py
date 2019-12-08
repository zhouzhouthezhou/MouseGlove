import IMUclass

def run():
	print("RUN: main.py")
	imu = IMUclass.IMU()
	while(True):
		imu.orientation()

if __name__ == '__main__':
	run()
