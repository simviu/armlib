import json
import numpy as np
#import cv2
#---------------
# utils
#---------------


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
        return {'t':str(self.t), 'e':str(self.e)}
    
    def dec(self, s):
        j = json.loads(s)
        self.t = j['t']
        return j


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
    T.t = T.t + dt

    print("T2 enc str:"+T.str())
    #---
    T.t = T.t + dt
    T.dec(s1)
    print("s1 dec result:"+T.str())
    return 

#----------
# main
#----------
if __name__ == "__main__":
    test()