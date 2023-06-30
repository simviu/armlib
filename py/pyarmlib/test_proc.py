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
#    for s in p.stdout:
#        print(s)

                     
print("   subprocess.Popen() ok")

while True:
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
    
