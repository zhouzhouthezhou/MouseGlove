import sys
# import mock
import math
import time
import struct
from machine import Pin, I2C, ADC
# from tools import MockSMBus

CHIP_ID = 0xEA
imuAdd = 0x69
bankSelect = 0x7f
bank = 0

GYRO_SMPLRT_DIV = 0x00
GYRO_CONFIG_1 = 0x01
GYRO_CONFIG_2 = 0x02

ACCEL_CONFIG = 0x14
ACCEL_XOUT_H = 0x2D
ACCEL_YOUT_H = 0x2F
ACCEL_ZOUT_H = 0x31
GYRO_XOUT_H = 0x33
GYRO_YOUT_H = 0x35
GYRO_ZOUT_H = 0x37

print('hello world')
i2c = I2C(scl=Pin(23), sda=Pin(22), freq=400000)

def config():
	test = i2c.scan()
	print("Connected I2C Devices:",test)

def selectBank(value):
	if not bank == value:
		i2c.writeto_mem(imuAdd, bankSelect, value << 4)
		bank = value
		print("Selected Bank on Device x69:", i2c.readfrom_mem(imuAdd, bankSelect, 1))
	print("Bank not changed")

def test():
	selectBank(0)
	i2c.readfrom_mem(imuAdd, ACCEL_XOUT_H)

	ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))

	selectBank(2)

def read_accelerometer_gyro_data():
	selectBank(0)
	i2c.readfrom_mem(imuAdd, ACCEL_XOUT_H)

	ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))

	selectBank(2)

	# Read accelerometer full scale range and
	# use it to compensate the self.reading to gs
	
	scale = (i2c.readfrom(ICM20948_ACCEL_CONFIG,8) & 0x06) >> 1

	# scale ranges from section 3.2 of the datasheet
	gs = [16384.0, 8192.0, 4096.0, 2048.0][scale]

	ax /= gs
	ay /= gs
	az /= gs

	# Read back the degrees per second rate and
	# use it to compensate the self.reading to dps
	scale = (i2c.readfrom(ICM20948_GYRO_CONFIG_1,8) & 0x06) >> 1

	# scale ranges from section 3.1 of the datasheet
	dps = [131, 65.5, 32.8, 16.4][scale]

	gx /= dps
	gy /= dps
	gz /= dps

	return ax, ay, az, gx, gy, gz

def orientation():
    # smbus = mock.Mock()
    # smbus.SMBus = MockSMBus
    # sys.modules['smbus'] = smbus

   # from icm20948 import ICM20948
   # icm20948 = ICM20948()
   # ax, ay, az, gx, gy, gz = icm20948.read_accelerometer_gyro_data()

    previous_RxEst_initial = 0
    previous_RyEst_initial = 0
    previous_RzEst_initial = 1
    mag_Rest_initial = math.sqrt(math.pow(previous_RxEst_initial,2) + math.pow(previous_RyEst_initial,2) + math.pow(previous_RzEst_initial,2))
    previous_RxEst = (previous_RxEst_initial / mag_Rest_initial)
    previous_RyEst = (previous_RyEst_initial / mag_Rest_initial)
    previous_RzEst = (previous_RzEst_initial / mag_Rest_initial)
    previous_RateAxz = 0
    previous_RateAyz = 0
    previous_Axz = math.atan2(previous_RxEst , previous_RzEst)
    previous_Ayz = math.atan2(previous_RyEst , previous_RzEst)
    RxEst_norm = 0
    RyEst_norm = 0
    RzEst_norm = 0
    while True:
        #from icm20948 import ICM20948
        #icm20948 = ICM20948()
        #ax, ay, az, gx, gy, gz = icm20948.read_accelerometer_gyro_data()
        ax, ay, az, gx, gy, gz = read_accelerometer_gyro_data()
        mag_Racc = math.sqrt(math.pow(ax,2) + math.pow(ay,2) + math.pow(az,2))
        ax_norm = ax / mag_Racc
        ay_norm = ay / mag_Racc
        az_norm = az / mag_Racc
        RateAxz = gy
        RateAyz = -gx
        RateAxz_avg = (RateAxz + previous_RateAxz) / 2
        RateAyz_avg = (RateAyz + previous_RateAyz) / 2
        previous_RateAxz = RateAxz
        previous_RateAyz = RateAyz
        wGyro = 15
        Axz = previous_Axz + (RateAxz_avg * 2.5 * math.pow(10, -6))
        Ayz = previous_Ayz + (RateAyz_avg * 2.5 * math.pow(10, -6))
        previous_Axz = Axz
        previous_Ayz = Ayz
        RxGyro = 1 / math.sqrt(1 + math.pow((1 / math.tan(Axz)) , 2) * math.pow((1 / math.cos(Ayz)) , 2))
        RyGyro = 1 / math.sqrt(1 + math.pow((1 / math.tan(Ayz)) , 2) * math.pow((1 / math.cos(Axz)) , 2))
        if previous_RzEst < 0:
            RzGyro = - math.sqrt(1 - math.pow(RxGyro , 2) - math.pow(RyGyro , 2))
        else:
            RzGyro = math.sqrt(1 - math.pow(RxGyro , 2) - math.pow(RyGyro , 2))
        RxEst = (ax_norm + RxGyro * wGyro) / (1 + wGyro)
        RyEst = (ay_norm + RyGyro * wGyro) / (1 + wGyro)
        RzEst = (az_norm + RzGyro * wGyro) / (1 + wGyro)
        R = math.sqrt(math.pow(RxEst,2) + math.pow(RyEst,2) + math.pow(RzEst,2))
        RxEst_norm = RxEst / R
        RyEst_norm = RyEst / R
        RzEst_norm = RzEst / R
        print("X: " + str(RxEst_norm))
        print("\nY: " + str(RyEst_norm))
        print("\nZ: " + str(RzEst_norm))
        time.sleep_ms(30)
        previous_RxEst = RxEst_norm
        previous_RyEst = RyEst_norm
        previous_RzEst = RzEst_norm 

    # assert (round(ax, 2), round(ay, 2), round(az, 2), int(gx), int(gy), int(gz)) == (0.05, 0.11, 0.16, 3, 4, 5)
    # del icm20948
