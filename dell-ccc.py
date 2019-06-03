import random
import usb.core
import usb.util

class dellCCC:
	def __init__(self):
		# 0x08 turns off. 0x01 - 0x07 changes color
		self.colors = {
			"black": 0x08,
			"white": 0x07,
			"red": 0x01,
			"green": 0x02,
			"blue": 0x03,
			"yellow": 0x04,
			"cyan": 0x06,
			"magenta": 0x05
		}

		# Specific USB
		self.dev = usb.core.find(idVendor=0x04d8, idProduct=0x0b28)

		# What we'll send to the USB
		self.array = [0x11]

		# IDK why but we need to fill an array with 255
		for x in range(1, 63):
			self.array.insert(x, 0xff)

		# https://stackoverflow.com/questions/29345325/raspberry-pyusb-gets-resource-busy#29370091
		if self.dev.is_kernel_driver_active(0):
		    self.dev.detach_kernel_driver(0)

		self.cfg = self.dev.get_active_configuration()
		self.intf = self.cfg[(0,0)]

		self.ep = usb.util.find_descriptor(
		    self.intf,
		    # match the first OUT endpoint
		    custom_match = \
		    lambda e: \
			usb.util.endpoint_direction(e.bEndpointAddress) == \
			usb.util.ENDPOINT_OUT)

	# We'll use this for checksumming
	def calculateCheckSum(self):
		return (21 * self.array[0] * self.array[0] + 19 * self.array[1] - 3 * self.array[3]) % 255


	def set_random_bits(self):
		# random for 'security'
		self.array[3] = int((random.random() * 256) % 255)
		self.array[2] = self.calculateCheckSum()

	def change_color(self, color):
		self.array[1] = self.colors[color]
		self.set_random_bits()
		self.ep.write(self.array)

	def random_color(self):
		color, null = random.choice(list(self.colors.items()))
		self.change_color(color)

	def disco(self):
		while True:
			self.random_color()



