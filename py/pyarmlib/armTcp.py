
import socket
import time


HOST = "127.0.0.1" 
PORT = 8192  


#-------------
# ArmTcp
#-------------
class ArmTcp:
    def __init__(self, sName):
        self.sName = sName

    #----    
    def connect(self, sHost=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.sock is None:
            print("socket failed")
            return false
        
            self.sock.connect((sHost, port))
    
        scmd = "init arm=z1"
        sock.sendall(bytes(scmd, "utf-8"))
        time.sleep(1)
        
       
