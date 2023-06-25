# Tcp server for mycobot.
# Dependencies: pip install pymycobot

import socket
import sys
import numpy as np
import time
import json

from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord
from port_setup import setup


HOST = ''  
PORT = 8192
K_spd_scl = 100
K_spd_max_mc = 100 # mycobot spd max 100
K_spd_dflt = 50

K_pose_readyPick = [160, -100, 100, -80, 22, -160]
#K_pose_rst = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

K_pose_t1 = [120, -100, 80, -70, 42, -175]
K_pose_t2 = [140, -80, 100, -60, 20, -170]
K_pose_t3 = [140, -100, 100, -80, 22, -160]

#-----
def pose2vec(T):
    t = T.t
    e = T.e
    v = [t[0],t[1],t[2],e[0],e[1],e[2]]
    return v
#-----
def vec2pose(v):
    T = Trans()
    T.t[0] = v[0]
    T.t[1] = v[1]
    T.t[2] = v[2]
    T.e[0] = v[3]
    T.e[1] = v[4]
    T.e[2] = v[5]
    return T

#----------
# ArmMyCobot
#----------
class ArmMyCobot():
    def __init__(self, port):
        self.cfg_ =[]
        self.cfg_['spd'] = K_spd_dflt
        return
    
    #----
    def init(self):
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

    #-----
    def getSt(self):
        mc = self.mc_
        pv = mc.get_coords()
        ans = mc.get_angles()
        st = ArmSt()
        st.T = vec2pose(pv)
        i = 0
        for a in ans:
            st.angles[i] = ans[i]
            i = i + 1

    #----
    def setJoints(self, angles, grip):
        spd = self.cfg_['spd']
        mc = self.mc_
        mc.send_coords(angles, spd, 0)
        sr = ''
        return True, sr
    
#----------
# tests
# ---------
def test1():
    arm = ArmMyCobot()
    arm.init()

    #----
    tip = TipSt()
    tip.T = vec2pose(K_pose_t1)
    arm.moveTo(tip)
    
    #----
    time.sleep(5)
    st = arm.getSt()
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
    mc.send_coords(K_pose_t1, spd, 0)
    time.sleep(5)

    print("pose t2")
    mc.send_coords(K_pose_t2, spd, 0)
    time.sleep(5)

    print("pose t3")
    mc.send_coords(K_pose_t3, spd, 0)
    time.sleep(5)

#----------
# main
#----------


if __name__ == "__main__":
   # test2()

    svr = ArmMyCobot(PORT)
    svr.run()

    
