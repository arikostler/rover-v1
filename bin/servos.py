import time
from darkwater_640 import dw_Controller, dw_Servo

dw = dw_Controller( addr=0x60 )

s1 = dw.getServo(1) # pitch
s2 = dw.getServo(2) # yaw

s1.off()
s2.off()

s2.setPWMuS(1900)

s1.off()
s2.off()
