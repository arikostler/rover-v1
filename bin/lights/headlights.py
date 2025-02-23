#!/usr/bin/python
import smbus
import time



class BrightPi:
	bus = smbus.SMBus(1)
	address = 0x70
	registers = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
	
	def __init__(self):
		self.name = "BrightPi_Default"
		self.bus.write_byte_data(self.address, 0x00, 0xff)
		self.bus.write_byte_data(self.address, 0x09, 0x00)
		self.bus.write_byte_data(self.address, 0x00, 0x00)

	def setName(self, newName):
		self.name = newName

	def setMode(self, newMode):
		self.mode = newMode

	def setI2CAddress(self, newAddress):
		self.address = newAddress

	def allOn(self):
		self.bus.write_byte_data(self.address, 0x00, 0xff)

	def allOff(self):
		self.bus.write_byte_data(self.address, 0x00, 0x00)

	def setGain(self, gain):
		# Can use hex or decimal. 
		# If using hex, use values between 0x00 and 0x0f
		# If using decimal, it works best with values between 0 and 15
		self.bus.write_byte_data(self.address, 0x09, gain)

	def write(self, light, brightness):
		self.bus.write_byte_data(self.address, light, brightness)

	def getIRRegisters(self):
		return [0x01, 0x03, 0x06, 0x08]

	def getWhiteRegisters(self):
		return [0x02, 0x04, 0x05, 0x07]

	def getAllLightRegisters(self):
		return [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

lights = BrightPi()

whites = lights.getWhiteRegisters()
lights.allOn()

for y in range(20):
	for x in range(len(whites)):
		d = 0
		if (x == 0):
			d = len(whites)-1
		else:
			d = x-1
		print(whites[x])
		lights.write(whites[x], 255)
		time.sleep(.05)
		lights.write(whites[d], 0)
		time.sleep(.05)

lights.allOff()
