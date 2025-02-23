#!/usr/bin/python
import pygame
import time
import smbus
from darkwater_640 import dw_Controller, dw_Servo

def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def calculateMotorSpeeds(horizontal, vertical):
	speeds = [0,0]
	vertical *= -1
	speeds[0] = vertical + horizontal
	speeds[1] = vertical - horizontal
	return speeds

class BrightPi:
	bus = smbus.SMBus(1)
	address = 0x70
	registers = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
	
	def __init__(self):
		self.name = "BrightPi_Default"
		self.bus.write_byte_data(self.address, 0x00, 0xff)
		self.bus.write_byte_data(self.address, 0x09, 0x0f)
		self.bus.write_byte_data(self.address, 0x00, 0x00)
		# for x in range(1,8):
		# 	self.write(self.registers[x], 255)

	def setName(self, newName):
		self.name = newName

	def setMode(self, newMode):
		self.mode = newMode

	def setI2CAddress(self, newAddress):
		self.address = newAddress

	def allOn(self):
		self.bus.write_byte_data(self.address, 0x00, 0xff)
		self.setGain(0x0f)
		for x in range(1,8):
			self.write(self.registers[x], 255)

	def allOff(self):
		self.bus.write_byte_data(self.address, 0x00, 0x00)
		for x in range(1,8):
			self.write(self.registers[x], 0)

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

print("Preparing...")
dw = dw_Controller( addr=0x60 )

s1 = dw.getServo(1) # pitch
s2 = dw.getServo(2) # yaw
m1 = dw.getMotor(1)
m2 = dw.getMotor(2)

s1.off()
s2.off()
m1.off()
m2.off()

s1pos = 1500
s2pos = 1500

lights = BrightPi()
# lights.allOn()

pygame.init()
pygame.display.set_mode((1, 1))

pygame.joystick.init()

done = False
clock = pygame.time.Clock()

lightstate = False
lightlock = False
print("Ready!")
# twirl(lights)

while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released")

	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	s2pos = s2pos - int(round(joystick.get_axis(2)*20))
	s1pos = s1pos + int(round(joystick.get_axis(5)*20))
	m1js = int(round(joystick.get_axis(0)*10))
	m2js = int(round(joystick.get_axis(1)*10))
	if (joystick.get_button(5)==1):
		if (lightlock==False):
			if lightstate == False:
				lights.allOn()
				lightstate = True
			else:
				lights.allOff()
				lightstate = False
			lightlock = True
	else:
		lightlock = False

	if s1pos > 2000:
		s1pos = 2000
	elif s1pos < 1000:
		s1pos = 1000

	if s2pos > 2000:
		s2pos = 2000
	elif s2pos < 1000:
		s2pos = 1000
	s1.setPWMuS(s1pos)
	s2.setPWMuS(s2pos)
	motorSpeeds = calculateMotorSpeeds(arduino_map(m1js, -10, 10, -255, 255), arduino_map(m2js, -10, 10, -255, 255))
	m1.setMotorSpeed(motorSpeeds[0])
	m2.setMotorSpeed(motorSpeeds[1])
	# clock.tick(20)


s1.off()
s2.off()
pygame.quit()