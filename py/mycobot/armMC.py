# Tcp server for mycobot.
# Dependencies: pip install pymycobot

import socket
import sys
import numpy as np
import time
import json

sys.path.append("./pyarmlib")

from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord
from port_setup import setup
from pyarmlib import armLib
from pyarmlib import utils 

HOST = ''  
PORT = 8192
K_spd_scl = 100
K_spd_max_mc = 100 # mycobot spd max 100
K_spd_dflt = 50

#K_pose_readyPick = [160, -100, 100, -80, 22, -160]
#K_pose_rst = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

K_pose_t1 = [0.120, -0.100, 0.080, -70, 42, -175]
#K_pose_t2 = [140, -80, 100, -60, 20, -170]
#K_pose_t3 = [140, -100, 100, -80, 22, -160]

K_pose_t4 = [0.180, -0.080, 0.100, -60, 20, -170]

#-----
def pose2vec(T):
    t = T.t * 1000.0 # MyCobot use mm
    e = T.e
    v = [t[0],t[1],t[2],e[0],e[1],e[2]]
    return v

#-----
def vec2pose(v):
    print("[dbg]: v=", v)
    T = utils.Trans()
    T.t[0] = v[0]
    T.t[1] = v[1]
    T.t[2] = v[2]
    T.t = T.t*0.001
    T.e[0] = v[3]
    T.e[1] = v[4]
    T.e[2] = v[5]
    return T

#----------
# ArmMyCobot
#----------
class ArmMyCobot(armLib.Arm):
    def __init__(self):
        self.cfg_ ={}
        self.cfg_['spd'] = K_spd_dflt
        return
    
    #----
    def init(self):
        print("ArmMyCobot init")
        #---- setup mycobot
        self.mc_ = setup()
        
        #--- initial release
        self.mc_.release_all_servos()
        return True
    
    #----
    def set_grip(self, grip):
        #--- grip range from 0-1.0, 1.0 is full open
        # PWM range center at 1500
        e = 1500 + (grip-0.5) * 1000
        if grip:
            self.mc_.set_encoder(7, 1300)
        else:
            self.mc_.set_encoder(7, 2048)


    #------
    def moveTo(self, tip, spdIn=0.5):
        spd = spdIn * K_spd_scl
        if spd > K_spd_max_mc:
            spd = K_spd_max_mc
        s = "moveto: "+ tip.str() + ", spd="+str(spd)
        pv = pose2vec(tip.T)
        self.mc_.send_coords(pv, int(spd), 0)
        self.set_grip(tip.grip)
        print(s)
        return True

    #-----
    def getSt(self):
        mc = self.mc_
        #print("mc is:", mc)
        pv = mc.get_coords()
        ans = mc.get_angles()
        st = armLib.ArmSt()
        st.T = vec2pose(pv)
        i = 0
        for a in ans:
            st.angles[i] = ans[i]
            i = i + 1
        return True,st

    #----
    def setJoints(self, angles, grip):
        spd = self.cfg_['spd']
        mc = self.mc_
        mc.send_coords(angles, spd, 0)
        return True
    
#----------
# tests
# ---------
def test1():
    arm = ArmMyCobot()
    arm.init()

    #----
    tip = armLib.TipSt()
    tip.T = vec2pose(K_pose_t1)
    arm.moveTo(tip)
    
    #----
    time.sleep(5)
    ok,st = arm.getSt()
    if not ok:
        print("failed to getSt()")
        return False

    #----
    print("st=")
    print(st.str())
    return

#----
def test2():
    mc = setup()
    spd = 20
     
#    print("pose readyPick");
#    mc.send_coords(K_pose_readyPick, spd, 0)
#    time.sleep(5)

    print("pose t1")
    mc.send_coords(K_pose_t4, spd, 0)
    time.sleep(5)

#    print("pose t2")
#    mc.send_coords(K_pose_t2, spd, 0)
#    time.sleep(5)

#    print("pose t3")
#    mc.send_coords(K_pose_t3, spd, 0)
#    time.sleep(5)

#----------
# main
#----------


if __name__ == "__main__":
    test1()
#    test2()

    
