import time
import threading

import numpy as np
from pyarmlib.armLib import *
from pymycobot import MyCobotSocket
from port_setup import setup
from pyarmlib.armServer import ArmServer
#-------------
# ArmMyCobot
#-------------
class ArmMyCobot(ArmServer):
    def __init__(self):
        self.k_spd = 20 # 1-100

        return

    #---- overide
    def init(self):
        print("ArmMyCobot init ok")
        self.mc = setup()
        return True,""
    
    def getSt(self):
        st = ArmSt()
        return True, st

    def moveTo(self, tipSt):
        return True 

    def setJoints(self, angles, grip):
        self.mc.sync_send_angles(angles, self.k_spd)
        self.set_grip(grip)
        return True

    #----
    def set_grip(self, grip):
        #--- grip range from 0-1.0, 1.0 is full open
        # PWM range center at 1500
        e = 1500 + (grip-0.5) * 1000
        #self.mc.set_encoder(7, e, self.k_spd)

#----------
# test
#----------
def test():
    arm = ArmMyCobot()
    arm.init()      
    #time.sleep(2)  
    #st = arm.getSt()
    #print("got st"+ st.str())
    #time.sleep(2)
    #----
    arm.setJoints([15, 0, 100, 10, -5 ,10], 0.5)
    time.sleep(5)

#----------
# main
#----------
if __name__ == "__main__":
    test()

    
