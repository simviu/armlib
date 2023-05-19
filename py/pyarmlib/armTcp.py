
import socket
import time


HOST = "127.0.0.1" 
PORT = 8192  

LN_MAX_CHARS = 2048

#-------------
# ArmTcp
#-------------
class ArmTcp:
    def __init__(self):
        self.sock_ = None
        return

    #----
    def recvLn(self):
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
        return self.sendCmd("init arm="+sName)
        
        
    #-----
    def sendCmd(self, scmd):
        self.sock_.sendall(bytes(scmd+"\n", "utf-8"))
        print("cmd sent:"+scmd)
        time.sleep(1)      
        
        sLn = self.recvLn()
        print("Recv ack:"+sLn)  
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

    
       
