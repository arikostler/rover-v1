import time
from darkwater_640 import dw_Controller, dw_Servo

dw = dw_Controller( addr=0x60 )

s1 = dw.getServo(1) # pitch
s2 = dw.getServo(2) # yaw

s1.off()
s2.off()

s1.setPWMuS(1100)
s2.setPWMuS(1600)
time.sleep(1)

s1.off()
s2.off()
