from machine import UART


class UartCom:
	def __init__(self):
		self.uart = UART.init(9600, bits = 8, parity=None, stop=1, tx=32, rx=35)

	def send_Message(self, message):
		self.uart.write(message)		
