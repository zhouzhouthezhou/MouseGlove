from machine import I2C

class IMU:
	imuAddress = 0x69
	bankSelect = 0x7f


	def __init__(self):
		self.bank = 0
		self.i2c = I2C(scl=Pin(23), sda=Pin(22), freq=400000)
		devices = self.i2c.scan()
		print("Connected I2C Devices", devices)

	def selectBank(self, value):
		if not self.bank == value:
			self.i2c.writeto_mem(imuAddress, bankSelect, value << 4)
			self.bank = value
			print("Selected Bank on Device x69:", i2c.readfrom_mem(imuAdd, bankSelect, 1))

	def test():
		selectBank(0)
		selectBank(2)
