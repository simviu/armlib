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
# Arm tip st
class TipSt:
    def __init__(self):
        self.t = np.array([0,0,0])
        self.e = np.array([0,0,0])
        self.grip = 0
    
    def parse(self,kvs):
        self.t = np.fromstring(kvs["xyz"], sep=',')
        self.e = np.fromstring(kvs["rvec"], sep=',')
        self.gr = float(kvs['grip'])

    def str(self):
        s = "t="+ str(self.t) +", e="
        s = s + str(self.e) + ", grip="
        s = s + str(self.gr)
        return s

    def pose_vec(self):
        t = self.t
        e = self.e
        v = [t[0],t[1],t[2],e[0],e[1],e[2]]
        return v


#----------
def parse_cmdln(s):
    ss = s.split(' ')
    cmd = ss.pop(0)
    kvs={}
    for s in ss:
        print('  s:"'+s+'"')
        k,v = s.split('=')
        kvs[k] = v
    return cmd,kvs

#----------
# ArmServer
#----------
class ArmServer():
    def __init__(self, port):
        #---- setup mycobot
        self.mc_ = setup()
        
        #--- initial release
        self.mc_.release_all_servos()

        #---- socket server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('# Socket created')
        # Create socket on port
        try:
            s.bind((HOST, port))
        except socket.error as msg:
            print('# Bind failed. ')
            sys.exit()

        print('# Socket bind complete')

        # Start listening on socket
        s.listen(10)

        print('Socket server now listening on port '+str(port)+'...')
        self.sock_ = s

    #----
    def set_grip(self, grip):
        #--- grip range from 0-1.0, 1.0 is full open
        # PWM range center at 1500
        e = 1500 + (grip-0.5) * 1000
        if grip:
            self.mc_.set_encoder(7, 1300)
        else:
            self.mc_.set_encoder(7, 2048)

    #--------------
    def run(self):
        s = self.sock_
        # Wait for client
        print("run() wait connection...")
        conn, addr = s.accept()
        print('  connected to ' + addr[0] + ':' + str(addr[1]))

        # Receive data from client
        while True:     
            data = conn.recv(1024)
            scmd = data.decode('UTF-8')    # convert to string (Python 3 only)
            if scmd == '':
                continue

            print( "recv:"+scmd )     
            #--- run command
            ok, jres = self.run_cmd(scmd)

            #--- acka
            sr = json.dumps(jres) + "\n" 
            print("sending ["+sr+"]...")
            conn.send(bytes(sr, "utf-8"))
            print("  sent")

        #s.close()
    #------
    def run_cmd(self, scmd):
        ok = True
        print("run cmd:"+scmd)
        jr = {"ok":True}
        jres = {}
        cmd,kvs = parse_cmdln(scmd)
        if cmd == "moveto":
            self.moveto(kvs)
        elif cmd == "release":
            self.mc_.release_all_servos()
        elif cmd == "st":
            jres = self.enc_st()
        jr["res"] = jres
        return ok, jr
    #------
    def enc_st(self):
        jres = {}

        v = self.mc_.get_coords()
        if len(v) < 6 :
            return jres

        jt = str(v[0])+","+str(v[1])+","+str(v[2])
        je = str(v[3])+","+str(v[4])+","+str(v[5])
        jT = {}
        jT["t"] = jt
        jT["e"] = je

        jtip = {}
        jtip["T"] = jT
        jst = {}
        jst["tip"] = jtip

        jres["st"] = jst
        return jres


    #------
    def moveto(self, kvs):
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

    svr = ArmServer(PORT)
    svr.run()

    
