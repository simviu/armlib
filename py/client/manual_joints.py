import socket
import sys
import time

HOST, PORT = "localhost", 8192


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock is None:
    print("Socket failed")
    exit(1)

print("Socket client connected to:"+HOST+":"+str(PORT))
# Connect to server and send data
sock.connect((HOST, PORT))

#-----
def send_cmd(scmd):

    print("sending :'"+scmd+"'")
    scmd1 = scmd + "\n"
    sock.sendall(bytes(scmd1, "utf-8"))
    # Receive data from the server and shut down
    s = str(sock.recv(1024), "utf-8")
    print("recv:"+s)


#---- main
send_cmd("init arm=z1")
send_cmd("st")
send_cmd("setJoints angles=0,50,-20,-20,0,-5 grip=1 t=2")
send_cmd("st")

time.sleep(5)
