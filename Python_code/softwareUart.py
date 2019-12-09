from machine import UART
import time


class UartCom:
	def __init__(self):
		self.uart = UART(1, 9600)
		self.uart.init(9600, bits = 8, parity=None, stop=1, rx=35, tx = 32, timeout=5000)

	def send_Message(self):
		while(True):
			self.uart.write('Fuck you Kyle')
			time.sleep(2)
		#self.uart.write('t')		
