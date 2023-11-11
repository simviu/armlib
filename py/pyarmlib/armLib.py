import utils
from utils import *

N_joints_dummy = 6
#-------------
class TipSt:
    def __init__(self):
        self.T = Trans()
        self.grip = 0.0
    
    def dec(self, j):
        self.T.dec(j['T'])
        self.grip = float(j['grip'])
    
    def str(self):
        s = "{"
        s = "'T':"+self.T.str() + ", "
        s = s + ", 'grip':" + str(self.grip)
        s = s + "}"
        return s

#-------------
class ArmSt:
    def __init__(self):
        self.tipSt = TipSt()
        self.angles = np.zeros((N_joints_dummy), dtype=float)
        self.ok = False
        self.sInfo = "N/A"
        return

    #---- 
    def dec(self, j):
        self.tipSt.dec(j["tip"])
        self.angles = np.array(j['angles'])
        #print("[dbg]: dec() angles :")
        #print(self.angles)
        return

    #---
    def str(self):
        s = "{"
        s = s + self.tipSt.str() + ", "
        s = s + "'angles':" + np2s(self.angles) 
        s = s + "}"
        return s

    
#-------------
class Arm(object):
    def __init__(self):
        return
    
    #---- dummy cmds
    def init(self):
        print("Arm dummy init ok")
        return True,""
    
    def getSt(self):
        st = ArmSt()
        return True, st

    def moveTo(self, tipSt):
        return True 

    def setJoints(self, angles, grip):
        return True
