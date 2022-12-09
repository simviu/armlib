# Tcp server for mycobot.
# Dependencies: pip install pymycobot

import socket
import sys
import numpy as np

from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

HOST = ''  
PORT = 8192
K_spd_scl = 10
K_spd_max_mc = 100 # mycobot spd max 100

#----------
# Arm tip st
class TipSt:
    def __init__(self):
        self.t = np.array([0,0,0])
        self.e = np.array([0,0,0])
        self.grip = 0

        self.mc_ = setup()

    
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
        v = [t[0],t[1],t[2],e[0].e[1].e[2]]
        

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

            print( "recv:"+scmd )     
            #--- run command
            ok, jres = self.run_cmd(scmd)

            #--- ack
            conn.send(bytes(jres, "utf-8"))

        #s.close()
    #------
    def run_cmd(self, scmd):
        ok = True
        print("run cmd:"+scmd)
        cmd,kvs = parse_cmdln(scmd)
        if cmd == "moveto":
            self.moveto(kvs)

        return ok, "{st:ok}"
    
    #------
    def moveto(self, kvs):
        ts = TipSt()
        ts.parse(kvs)
        spd = float(kvs["spd"]) * K_spd_scl
        if spd > K_spd_max_mc:
        	spd = K_spd_max_mc
        s = "moveto: "+ ts.str() + ", spd="+str(spd)
        pv = ts.pose_vec()
        self.mc_.send_coords(pv, spd, 0)
        self.set_grip(ts.gr)
        print(s)

#----------
# 
# ---------
def test():
    scmd = "moveto xyz=1.2,3.4,5.6 rvec=10.2,20.4,30.5 grip=0.00"
    print('scmd="'+scmd+'"')
    cmd,kvs = parse_cmdln(scmd)
    print("cmd:["+cmd+"]")
    ts = TipSt()
    ts.parse(kvs)
    print("ts={"+ts.str()+"}")


#----------
# main
#----------


if __name__ == "__main__":
   # test()

    svr = ArmServer(PORT)
    svr.run()

    
