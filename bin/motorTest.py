import time
from darkwater_640 import dw_Controller, dw_Servo

dw = dw_Controller( addr=0x60 )

m1 = dw.getMotor(1)
m2 = dw.getMotor(2)

m1.off()
m2.off()

m1.setMotorSpeed(255)
m2.setMotorSpeed(-255)

time.sleep(5)

m1.off()
m2.off()

time.sleep(1)

m1.setMotorSpeed(-255)
m2.setMotorSpeed(255)

time.sleep(5)

m1.off()
m2.off()
