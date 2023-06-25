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

K_pose_readyPick = [160, -100, 100, -80, 22, -160]
#K_pose_rst = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

K_pose_t1 = [120, -100, 80, -70, 42, -175]
K_pose_t2 = [140, -80, 100, -60, 20, -170]
K_pose_t3 = [140, -100, 100, -80, 22, -160]



#----------
# ArmMyCobot
#----------
class ArmMyCobot():
    def __init__(self, port):

        return
    
    #----
    def init(self):
        #---- setup mycobot
        self.mc_ = setup()
        
        #--- initial release
        self.mc_.release_all_servos()
        return 
    
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
    def moveTo(self, kvs):
        ts = TipSt()
        ts.parse(kvs)
        spd = float(kvs["spd"]) * K_spd_scl
        if spd > K_spd_max_mc:
            spd = K_spd_max_mc
        s = "moveto: "+ ts.str() + ", spd="+str(spd)
        pv = ts.pose_vec()
        self.mc_.send_coords(pv, int(spd), 0)
        self.set_grip(ts.gr)
        print(s)

    #-----
    def getSt(self):
        with self.st_lock_:
            return True,self.st_

    #----
    def setSt(self, st):
        ok = True
        g = st.tipSt.grip
        sj = np2s(st.joints)
        # cmd e.g.:
        #   setJoints angles=30,10,-20,20,20,-15 grip=1 t=2

        s = "setJoints "
        s = s + "angles=" + sj+" "
        s = s + "grip="+str(g)+" "
        s = s+ "t=" + str(DFLT_setJoints_t)

        return self.sendCmd_(s)
#----------
# tests
# ---------
def test1():
    scmd = "moveto xyz=1.2,3.4,5.6 rvec=10.2,20.4,30.5 grip=0.00"
    print('scmd="'+scmd+'"')
    cmd,kvs = parse_cmdln(scmd)
    print("cmd:["+cmd+"]")
    ts = TipSt()
    ts.parse(kvs)
    print("ts={"+ts.str()+"}")

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

    
