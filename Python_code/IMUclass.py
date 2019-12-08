import struct

from machine import I2C, Pin

class IMU:
	imuAddress = 0x69
	bankSelect = 0x7f

	accelXhigh = 0x2D
	gyroXhigh = 0x33


	def __init__(self):
		self.bank = 0
		self.i2c = I2C(scl=Pin(23), sda=Pin(22), freq=400000)
		devices = self.i2c.scan()
		print("Connected I2C Devices", devices)

	def readFrom(self, address, byteNum):
		return self.i2c.readfrom_mem(self.imuAddress, address, byteNum)

	def selectBank(self, value):
		value = value << 4
		print(self.bank, value, bytes([value]))
		if self.bank != value:
			self.i2c.writeto_mem(self.imuAddress, self.bankSelect, bytes([value]))
			self.bank = value
			print("Selected Bank on Device x69:", self.readFrom(self.bankSelect, 1))
		else:
			print("Bank value not changed")

	def test(self):
		print("selecting bank 0")
		self.selectBank(0)
		data = self.readFrom(self.accelXhigh, 12)
		ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))
		print(ax, ay, az, gx, gy, gz)
		print("selecting bank 2")
		self.selectBank(2)

