from machine import UART


class UART:
	def __init__(self):
		self.uart = uart.init(115200, bits = 114, parity=None, stop=1, tx=32, rx=35, rts=-1, cts=-1, txbug=256, rts=256,timeout=5000)

	def send_Message(self, message):
		self.uart.write(message)
