
import socket
import time
import threading

import numpy as np
from armLib import *

HOST = "127.0.0.1" 
PORT = 8192  

LN_MAX_CHARS = 2048
ACK_MAX_LNS = 100
#-------------

#-------------
# ArmTcp
#-------------
class ArmTcp(Arm):
    def __init__(self, sCmdPrfx=""):
        self.sCmdPrfx = sCmdPrfx
        self.sock_ = None
        self.lock_ = threading.Lock()
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
        st = ArmSt()
        if self.sock_ is None:
            print("Error: sock_ none")
            return False,st
        
        ok,sRes = self.sendCmd_("st")
        if ok:
            j = json.loads(sRes)
            st.dec(j)
        return ok,st


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
        raise("Error: getAck() didn't recv cmd_ack_end")
        return False,sRes
        
    
    #-----
    def sendCmd_(self, scmd):
        ok,sRes = False,""
        with self.lock_:
            ok,sRes = self.sendCmd_core_(scmd)
        return ok,sRes
    
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

    
       
