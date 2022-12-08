import socket
import sys

HOST = ''  
PORT = 8192

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

    #--------------
    def run(self):
        s = self.sock_
        # Wait for client
        print("run() wait connection...")
        conn, addr = s.accept()
        print('  connected to ' + addr[0] + ':' + str(addr[1]))

        # Receive data from client
        i=0
        while True:     
            data = conn.recv(1024)
            line = data.decode('UTF-8')    # convert to string (Python 3 only)

            print( "recv:"+line )     
            #--- echo
            s = "ack " + str(i)
            i = i + 1
            conn.send(bytes(s, "utf-8"))

        #s.close()



#----------
# main
#----------


if __name__ == "__main__":
    svr = ArmServer(PORT)
    svr.run()

    