import struct
import time
import math

from machine import I2C, Pin

class IMU:
	#bank0
	chipID = 0xEA
	whoAmI = 0x00
	usrCtrl = 0x03
	pinConfig = 0x0F
	imuAddress = 0x69
	bankSelect = 0x7f


	pwr1 = 0x06
	pwr2 = 0x07

	accelXhigh = 0x2D
	gyroXhigh = 0x33

	#bank2
	gyroSmpl = 0x00
	gyroConfig1 = 0x01
	gyroConfig2 = 0x02

	accelSmpl1 = 0x10
	accelSmpl2 = 0x11
	accelCtrl = 0x12
	accelThr = 0x13
	accelConfig = 0x14

	#bank3
	i2cMstCtrl = 0x01
	i2cMstDelay = 0x02

	def __init__(self):
		self.bank = -1
		self.i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
		devices = self.i2c.scan()
		print("Connected I2C Devices", devices)
		self.config()

	def config(self):
		self.selectBank(0)

		#check if imu is connected
		#if self.readFrom(self.whoAmI, 1) != self.chipID:
		#	raise RuntimeError("Unable to find IMU")

		#turn imu on
		self.writeTo(self.pwr1, 0x01)
		self.writeTo(self.pwr2, 0x00)

		self.selectBank(2)

		#set gyro sample rate
		gyroRate = int((1100.0 / 100) - 1)
		self.writeTo(self.gyroSmpl, gyroRate)

		#set gyro lowpass
		gconfig1 = struct.unpack('>B', self.readFrom(self.gyroConfig1, 1))[0] & 0b10001110
		gconfig1 |= 0b1
		gconfig1 |= (5 & 0x07) << 4
		self.writeTo(self.gyroConfig1, gconfig1)

		#set gyro full scale
		gfullscale = struct.unpack('>B', self.readFrom(self.gyroConfig1, 1))[0] & 0b11111001
		gfullscale |= {250: 0b00, 500: 0b01, 1000: 0b10, 2000: 0b11}[250] << 1
		self.writeTo(self.gyroConfig1, gfullscale)

		#set accelerometer sample rate
		aRate = int((1125.0 / 1125) - 1)
		self.writeTo(self.accelSmpl1, (aRate >> 8) & 0xff)
		self.writeTo(self.accelSmpl2, aRate & 0xff)


		#set accelerometer lowpass
		aconfig = struct.unpack('>B', self.readFrom(self.accelConfig, 1))[0] & 0b10001110
		aconfig |= 0b1
		aconfig |= (5 & 0x07) << 4
		self.writeTo(self.accelConfig, aconfig)

		#set accelerometer 
		afullscale = struct.unpack('>B', self.readFrom(self.accelConfig, 1))[0] & 0b11111001
		afullscale |= {2: 0b00, 4: 0b01, 8: 0b10, 16: 0b11}[16] << 1
		self.writeTo(self.accelConfig, afullscale)

		self.selectBank(0)
		self.writeTo(self.pinConfig, 0x30)
		self.writeTo(self.usrCtrl, 0x20)

		self.selectBank(3)
		self.writeTo(self.i2cMstCtrl, 0x4D)
		self.writeTo(self.i2cMstDelay, 0x01)
		

	def writeTo(self, address, buff):
		self.i2c.writeto_mem(self.imuAddress, address, bytes([buff]))

	def readFrom(self, address, byteNum):
		return self.i2c.readfrom_mem(self.imuAddress, address, byteNum)

	def selectBank(self, value):
		value = value << 4
		if self.bank != value:
			print("selecting bank ", value >> 4)
			self.writeTo(self.bankSelect, value)
			self.bank = value
			print("Selected Bank on Device x69:", self.readFrom(self.bankSelect, 1))
		else:
			print("Bank value not changed")

	def silentSelectBank(self, value):
		value = value << 4
		if self.bank != value:
			self.writeTo(self.bankSelect, value)
			self.bank = value

	def readAccelerometerGyroData(self):
		self.silentSelectBank(0)
		data = self.readFrom(self.accelXhigh, 12)
		ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))

		self.silentSelectBank(2)

		scale = (struct.unpack('>B', self.readFrom(self.accelConfig, 1))[0] & 0x06) >> 1

		gs = [16384.0, 8192.0, 4096.0, 2048.0][scale]

		ax /= gs
		ay /= gs
		az /= gs

		scale = (struct.unpack('>B', self.readFrom(self.gyroConfig1, 1))[0] & 0x06) >> 1

		dps = [131.0, 65.5, 32.8, 16.4][scale]

		gx /= dps
		gy /= dps
		gz /= dps

		return (ax, ay, az, gx, gy, gz)

	def orientation(self):
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
	        ax, ay, az, gx, gy, gz = self.readAccelerometerGyroData()
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
	        print("Y: " + str(RyEst_norm))
	        print("Z: " + str(RzEst_norm))
	        time.sleep_ms(30)
	        previous_RxEst = RxEst_norm
	        previous_RyEst = RyEst_norm
	        previous_RzEst = RzEst_norm 
