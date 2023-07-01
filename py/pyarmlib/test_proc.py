import time
import shlex
import subprocess as sp
from threading import Thread


print("Run cmd:")
p = sp.Popen(["./tmp.sh"],
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     text=True
                     ) 
                     #as p :
print("Popen Ok")                     

for s in p.stdout:
    if s is None:
        print("None")
    elif s == "":
        print("empty")
        
    print("----")
    print(s)
    time.sleep(0.2)    

                     
print("   subprocess.Popen() ok")

while False:
    sOut, sErr = p.communicate()
    print("[dbg]---- sOut ----")
    print(sOut)
    print("[dbg]---- sErr ----")
    print(sErr)
    time.sleep(0.5)

    #output = p.stdout.read() # <-- Hangs here!
    #if not output:
    #    print('[No more data]')
    #    break
    #print(output)
    
