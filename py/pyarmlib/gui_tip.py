import tkinter as tk
from tkinter import ttk
from armTcp import *
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
        self.lTitle_ = tk.Label(topFrm, text = "Tip Control pannel")
        self.lTitle_.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        frm.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frm  = frm


        #----
        ctrl1 = Ctrl3Dof(frm, "pos",   self.onCtrlPos_)
        ctrl2 = Ctrl3Dof(frm, "Euler", self.onCtrlEuler_)
        ctrl1.frm.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        ctrl2.frm.grid(row=1, column=1, sticky=(tk.E,tk.W,tk.N,tk.S))

        ok,st = self.arm_.getSt()
        if not ok:
            print("Error:wrong status")
            return
        
        self.tipSt_ = st.tipSt
        self.update()
        return
    
    #---
    
    #----
    def onCtrlPos_(self, d):
        tst = self.tipSt_ 
        t = tst.T.t
        t = t + d * POS_D_SCL
        tst.T.t = t
        ok = self.arm_.moveTo(tst)
        return ok
    
    #----
    def onCtrlEuler_(self, d):
        tst = self.tipSt_ 
        e = tst.T.e
        e = e + d * EULER_D_SCL
        tst.T.e = e
        ok = self.arm_.moveTo(tst)
        return ok
   
    #---
    def update(self):
        return

#------------------
class TestApp:
    def __init__(self, root):
        #arm = None
        arm = ArmTcp()
        arm.connect(TEST_HOST, TEST_PORT)
        ok = arm.init('z1')
        
        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.lTitle_ = tk.Label(frm, text = "Test")
        self.lTitle_.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        self.tipPanel = TipPanel(frm, arm)
        self.frm = frm

#-------------------------
#    main 
#-------------------------
root = tk.Tk()
app = TestApp(root)
root.mainloop()

