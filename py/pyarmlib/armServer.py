
import socket
import time
import threading

import numpy as np
from armLib import *


HOST = ''  
PORT = 8192  

LN_MAX_CHARS = 2048
ACK_MAX_LNS = 100
T_GET_ST = 0.5


#-------------

#-------------
# ArmServer
#-------------
class ArmServer(Arm):
    def __init__(self, arm):
        self.arm_ = arm
        self.sock_ = None
        self.cmd_lock_ = threading.Lock()
        return

        
    #----    
    def init(self, port=PORT):
         #---- socket server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('# Socket created')
        # Create socket on port
        try:
            s.bind((HOST, port))
        except socket.error as msg:
            print('# Bind failed. ')
            return False

        print('# Socket bind complete')

        # Start listening on socket
        s.listen(10)

        print('Socket server now listening on port '+str(port)+'...')
        self.sock_ = s
        return True

    #--------------
    def run(self):
        s = self.sock_
        # Wait for client
        print("run() wait connection...")
        conn, addr = s.accept()
        print('  connected to ' + addr[0] + ':' + str(addr[1]))

        # Receive data from client
        while True:     
            scmd = self.recvLn_(conn)   
            if scmd == '':
                continue

            print( "recv scmd:'"+scmd+"'" )     
            #--- run command
            with self.cmd_lock_:
                ok, sres = self.run_cmd_(scmd)

            #--- send ack
            sr = "cmd_ack\n"
            sr = sr + "cmd_ok=" + "true" if ok else "false" + "\n"
            sr = sr + sres + "\n"
            sr = sr + "cmd_ack_end\n"
            conn.send(bytes(sr, "utf-8"))
            print("  sent ack:\n")
            print(sr)

    #------------- private -------------
    def recvLn_(self, conn):
        if self.sock_ is None:
            raise Exception('Not connected')

        #---- ref
        #    data = conn.recv(1024)
        #    scmd = data.decode('UTF-8')    # convert to string (Python 3 only)

        s = ""
        for i in range(LN_MAX_CHARS):
            #print("[dbg] recving...")
            b = conn.recv(1)
            c = b.decode('UTF-8')
            #print("[dbg] recv:'"+c+"'")
            if c == "\n":
                return s
            s = s + c

        return s

    #----
    def run_cmd_(self, scmd):
        if self.arm_ is None:
            print("[Error]: Arm is None")
            return False 
        
        #----
        ss = scmd.split(" ")
        if len(ss) == 0 :
            return False,"empty cmds"
        
        sc = ss[0]
        print("Recv cmd:'"+sc+"'")

        #-----
        ok, sr = False,""

        if sc== "init":
            ok,sr = self.arm_.init()

        elif sc == 'st':
            ok, st = self.arm_.getSt()
            sr = st.str()

        else :
            print("Unkown cmd:'"+sc+"'")
            sr = "Unkown"

        return ok,sr
            
#----------
# test
#----------
def test():
    arm = Arm()
    srvr = ArmServer(arm)
    if srvr.init():
        srvr.run()

    return False

#----------
# main
#----------
if __name__ == "__main__":
    test()

    
       
