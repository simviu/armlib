
import socket
import time


HOST = "127.0.0.1" 
PORT = 8192  

LN_MAX_CHARS = 1024

#-------------
# ArmTcp
#-------------
class ArmTcp:
    def __init__(self):
        return

    #----
    def recvLn(self):
        s = ""
        while True:
            c = str(sock.recv(1))
            if c == "\n":
                return s
            print("r:"+c)
            s = s + c
            
            
        
    #----    
    def connect(self, sHost=HOST, port=PORT):
        print("ArmTcp connect to '"+sHost+"'" + str(port)+"...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.sock is None:
            print("socket failed")
            return false
        
            self.sock.connect((sHost, port))
        
        # TODO: check connection
        print("connected")
        return
    
    #-----
    def init(self, sName):
        scmd = "init arm="+sName # e.g. : "z1"
        self.sock.sendall(bytes(scmd, "utf-8"))
        print("cmd sent:"+scmd)
        time.sleep(1)      
        
        sLn = self.recvLn()
        print("Recv ln:"+sLn)  
        time.sleep(1)
        return True # TODO: check st


#----------
# test
#----------
def test():
    arm = ArmTcp()
    arm.connect(HOST, PORT)
    arm.init("z1")      
    time.sleep(2)  

#----------
# main
#----------
if __name__ == "__main__":
    test()

    
       
