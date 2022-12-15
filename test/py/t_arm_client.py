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


scmd = "moveto xyz=-0.3,-0.1,0.4 rvec=180,0,0 spd=1 grip=-0.3"
scmd += "\n"
print("sending :'"+scmd+"'")
sock.sendall(bytes(scmd, "utf-8"))

# Receive data from the server and shut down
s = str(sock.recv(1024), "utf-8")
print("recv:"+s)

time.sleep(5)
