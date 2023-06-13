
import socket
import time
import threading

import numpy as np
from armLib import *


HOST = "127.0.0.1" 
PORT = 8192  

LN_MAX_CHARS = 2048
ACK_MAX_LNS = 100
T_GET_ST = 0.5

DFLT_setJoints_t = 2
#-------------

#-------------
# ArmTcp
#-------------
class ArmTcp(Arm):
    def __init__(self, sCmdPrfx=""):
        self.sCmdPrfx = sCmdPrfx
        self.sock_ = None
        self.cmd_lock_ = threading.Lock()
        self.st_lock_  = threading.Lock()
        self.st_ = ArmSt()

        #---- start thread of get st
        self.st_thread_ = threading.Thread(target=self.getSt_thd_,  daemon=True)
        self.st_thread_.start()
        return

        
    #----    
    def connect(self, sHost=HOST, port=PORT):
        print("ArmTcp connect to '"+sHost+"'" + str(port)+"...")
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.sock_ is None:
            raise Exception("socket failed")
        
        self.sock_.connect((sHost, port))
        
        # TODO: check connection
        print("connected")

    #-----
    def init(self, sName):
        return self.sendCmd_("init arm="+sName)
        
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

        ok = self.sendCmd_(s)
        return ok

    #---
    def moveTo(self, tipSt):
        s = "moveTo "
        s = s + "xyz=" + np2s(tipSt.T.t) + " "
        s = s + "euler=" + np2s(tipSt.T.e) + " " 
        s = s + "grip=" + str(tipSt.grip) 
        ok = self.sendCmd_(s)
        return ok
        

    #------------- private -------------
    def recvLn_(self):
        if self.sock_ is None:
            raise Exception('Not connected')
            
        s = ""
        for i in range(LN_MAX_CHARS):
            b = self.sock_.recv(1)
            c = b.decode('UTF-8')
            if c == "\n":
                return s
            #print("recv:"+c)
            s = s + c

        return s
            

    #-----
    def getAck_(self):
        ok = False
        sRes = ""
        bAck = False
        for i in range(ACK_MAX_LNS):
            s = self.recvLn_()
            if len(s) == 0:
                continue

            print("[dbg]:getAck_() got s='"+s+"'")
            ss = s.split("=")
            if ss[0] == "cmd_ack":
                bAck = True
            elif ss[0] == "cmd_ack_end":
                if not bAck:
                    print("Error: header 'cmd_ack' not found")
                    return False,sRes
                return ok,sRes
            elif ss[0] == "cmd_ok":
                ok = True if ss[1] == "true" else False
            else:
                sRes = sRes + s +"\n"
        #-----
        raise("Error: getAck() ACK_MAX_LNS reached, didn't recv cmd_ack_end")
        
    
    #-----
    def sendCmd_(self, scmd):
        ok,sRes = False,""
        with self.cmd_lock_:
            ok,sRes = self.sendCmd_core_(scmd)
        return ok,sRes
    
    #---- thread running at background, keep getting st
    def getSt_thd_(self):
        print("  thread of getSt_thd_ running...")
        while(True):
            st = ArmSt()
            ok,sRes = self.sendCmd_("st")
            if ok:
                j = json.loads(sRes)
                st.dec(j)
                st.sInfo = ""

            st.ok = ok
            with self.cmd_lock_:
                self.st_ = st

            time.sleep(T_GET_ST)            
        
    
    #----
    def sendCmd_core_(self, scmd):
        self.sock_.sendall(bytes(self.sCmdPrfx +" "+ scmd+"\n", "utf-8"))
        print("cmd sent:"+scmd)
        time.sleep(1)      
        
        #sLn = self.recvLn()
        #print("Recv ack:"+sLn)  
        ok,sRes = self.getAck_()
        sOk = "True" if ok else "False"
        print("cmd_ok:" + sOk)
        print("sRes:"+sRes)
        time.sleep(1)
        return ok, sRes


#----------
# test
#----------
def test():
    arm = ArmTcp()
    arm.connect(HOST, PORT)
    arm.init("z1")      
    time.sleep(2)  
    st = arm.getSt()
    print("got st"+ st.str())
    time.sleep(2)

#----------
# main
#----------
if __name__ == "__main__":
    test()

    
       
