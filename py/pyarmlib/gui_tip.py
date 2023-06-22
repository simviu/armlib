import tkinter as tk
import time
from tkinter import ttk
from armTcp import *
from gui_st import *
from utils import *

from threading import Thread
from functools import partial

import copy

#--- for test
TEST_HOST = "127.0.0.1"
TEST_PORT = 8192

#---
POS_D_SCL = 0.01
EULER_D_SCL = 5

T_SYNC_THREAD = 1.0
#------------------
# Ctrl3Dof
#------------------
# 0|           Label
# 1|    +y           +z
# 2| -x     +x
# 3|    -y           -z
# 4|
#  |  0  1   2   3    4
#
class Ctrl3Dof():
    def __init__(self, topFrm, sName, callbk):
        self.sName_ = sName
        self.callbk_ = callbk
        frm = ttk.Frame(topFrm, padding=(30,30,60,60))
        ss = ["+x", "-x", "+y", "-y", "+z", "-z"]

        #---- label
        self.lTitle_ = tk.Label(frm, text = sName)
        self.lTitle_.grid(row=0, column=3, sticky=(tk.E,tk.W,tk.N,tk.S))

        #--- [row,col] grid pair
        grids=np.array([[2,2],[2,0], [1,1], [3,1], [1,4], [3,4]])
        btns = []
        for i in range(6):
            b = tk.Button(frm, text=ss[i], command=partial(self.onButton, ss[i]))
            b.grid(row=grids[i,0], column=grids[i,1], sticky=(tk.E,tk.W,tk.N,tk.S))
            btns.append(b)

        self.btns_ = btns
        self.frm = frm
        frm.columnconfigure(3, minsize=20)
        frm.rowconfigure(0, minsize=80)
        return
    
    #----
    def onButton(self, sId):
        print("button pressed:"+sId)
        if self.callbk_ is None:
            return 
        d = np.array([0,0,0])
        if sId=="+x" : d[0] = 1.0
        if sId=="-x" : d[0] = -1.0
        if sId=="+y" : d[1] = 1.0
        if sId=="-y" : d[1] = -1.0
        if sId=="+z" : d[2] = 1.0
        if sId=="-z" : d[2] = -1.0
        
        self.callbk_(d)
        return

#---------------
# TipPanel
#---------------
class TipPanel():
    def __init__(self, topFrm, arm):
        self.arm_ = arm

        self.st_lock_  = threading.Lock()
        self.T_trgt_ = Trans()
        self.T_cur_ = Trans()

        #-----
        lt = tk.Label(topFrm, text = "Tip Control pannel")
        lt.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        frm.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frm  = frm
        #----
        ctrl1 = Ctrl3Dof(frm, "pos ctrl",   self.onCtrlPos_)
        ctrl2 = Ctrl3Dof(frm, "Euler ctrl", self.onCtrlEuler_)
        ctrl1.frm.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        ctrl2.frm.grid(row=1, column=1, sticky=(tk.E,tk.W,tk.N,tk.S))

        #----
        pst1 = StTipPanel(frm, "target")
        pst2 = StTipPanel(frm, "current")
        pst3 = StTipPanel(frm, "delta")
        pst1.frm.grid(row=2, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        pst2.frm.grid(row=3, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        pst3.frm.grid(row=4, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        
        self.pnl_trgt_  = pst1
        self.pnl_cur_   = pst2
        self.pnl_delta_ = pst3
        self.update()
        return
    
    #---
    
    #----
    def onCtrlPos_(self, d):
        with self.st_lock_:
            T = self.T_trgt_
            T.t = T.t + d * POS_D_SCL

        self.update()
        #ok = self.arm_.moveTo(tst)
        return True
    
    #----
    def onCtrlEuler_(self, d):
        with self.st_lock_:
            T = self.T_trgt_
            T.e = T.e + d * EULER_D_SCL

        self.update()
        return True
   
    #---
    def update(self):
        with self.st_lock_:
            T = self.T_trgt_
            print("T="+T.str())
            self.pnl_trgt_.set(T)
        return
    #----

    #-----------------
    def sync_thd_(self):
        print("  TipPanel::sync_thd_() thread started...")
        while True:

            #----- get st
            ok,st = self.arm_.getSt()
            if ok:
                self.st_ = st
                self.update()
            else :
                self.st_.ok = False
                print("TipPanel failed to get st")

            #---- chk target req

            #----
            time.sleep(T_SYNC_THREAD)
        return

#--------
def func_thd_test():
    while True:
        print("thd func run...")
        time.sleep(0.5)
    return

#------------------
class TestApp:
    def __init__(self, root):
        #arm = None
        arm = ArmTcp()
        if arm is not None:
            arm.connect(TEST_HOST, TEST_PORT)
            ok = arm.init('z1')

        lt = tk.Label(root, text = "Test")
        lt.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.tipPanel = TipPanel(frm, arm)
        self.frm = frm

        #---- st thread test
        #print("start st thread...")
        #self.st_thread_ = Thread(target=func_thd_test,  daemon=True)
        #self.st_thread_.start()
        #print("st thread running.")

#----------
# main
#----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()

