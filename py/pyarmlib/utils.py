import json
import numpy as np
#import cv2
#---------------
# utils
#---------------
def vec2s(v):
    return str(v[0]) + "," + str(v[1]) + "," + str(v[2])

#----
def dgrIn180(a):
        if a > 180:
            return 180
        elif a < -180:
            return -180
        return a
#-------------
class Trans:
    def __init__(self, 
                 t=np.array([0,0,0]),
                 e=np.array([0,0,0]) ):
        self.t = t
        self.e = e
        return
    
    def str(self):
        return str(json.dumps(self.enc()))

    def enc(self):
        return {'t':vec2s(self.t), 'e':vec2s(self.e)}
    
    def dec(self, s):
        j = json.loads(s)
        print("j[t]="+str(j['t']))
        self.t = np.fromstring(str(j['t']), sep=',')
        self.e = np.fromstring(str(j['e']), sep=',')
        return 


#----------
# test
#----------
def test():
    T = Trans(np.array([1,2,3]),
              np.array([10,20,30]))
    print("T1 enc str:"+T.str())
    s1 = T.str()
    #---
    dt = np.array([0.1,0.2,0.3])
    de = np.array([5,5,5])
    T.t = T.t + dt
    T.e = T.e + de
    print("T+dT:"+T.str())

    #---
    T.dec(s1)
    print("s1 dec result:"+T.str())
    return 

#----------
# main
#----------
if __name__ == "__main__":
    test()