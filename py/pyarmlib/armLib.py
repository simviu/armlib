from utils import *


#-------------
class TipSt:
    def __init__(self):
        self.T = Trans()
        self.grip = 0.0
    
    def dec(self, j):
        self.T.dec(j['T'])
        self.grip = float(j['grip'])

#-------------
class ArmSt:
    def __init__(self):
        self.tipSt = TipSt()
        self.joints = np.array([])
        return

    #---- 
    def dec(self, j):
        self.tipSt.dec(j["tip"])
        self.joints = np.array(j['joints'])
        #print("[dbg]: dec() joints :")
        #print(self.joints)
        return


    
#-------------
class Arm(object):
    def __init__(self):
        return