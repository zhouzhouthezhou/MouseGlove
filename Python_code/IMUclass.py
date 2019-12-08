import struct

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
		self.i2c = I2C(scl=Pin(23), sda=Pin(22), freq=400000)
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

	def test(self):
		data = self.readFrom(self.accelXhigh, 12)
		print(data)
		ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))
		#print("selecting bank 2")
		#self.selectBank(2)

