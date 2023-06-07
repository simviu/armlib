import tkinter as tk
from tkinter import ttk
from armTcp import *
from utils import *
from threading import Thread


#--- for test
TEST_HOST = "127.0.0.1"
TEST_PORT = 8192

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
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        ss = ["+x", "-x", "+y", "-y", "+z", "-z"]

        #---- label
        self.lTitle_ = tk.Label(topFrm, text = sName)
        self.lTitle_.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        #--- [row,col] grid pair
        grids=np.array([[2,2],[2,0], [1,1], [3,1], [1,4], [3,4]])
        btns = []
        
        for i in range(6):
            b = tk.Button(frm, text =ss[i], command=self.onButton)
            b.grid(row=grids[i,0], column=grids[i,1], sticky=(tk.E,tk.W,tk.N,tk.S))
            btns.append(b)

        self.btns_ = btns
        self.frm = frm
        return
    
    #----
    def onButton(self):
        print("button pressed")
        return

#---------------
# TipPanel
#---------------
class TipPanel():
    def __init__(self, topFrm, arm):
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        self.frm  = frm

        self.lTitle_ = tk.Label(frm, text = "Tip Control pannel")
        self.lTitle_.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))


        #----
        ctrl1 = Ctrl3Dof(frm, "pos", None)
        ctrl2 = Ctrl3Dof(frm, "Euler", None)
        ctrl1.frm.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))
        ctrl2.frm.grid(row=1, column=1, sticky=(tk.E,tk.W,tk.N,tk.S))

        return 
    
        #-----
        self.arm_ = arm
        self.st_ = ArmSt()
        ok,self.st_ = self.arm_.getSt()
        if ok:
            self.update()
        else:
            print("Error:wrong status")

        return
    #----
    def update(self):
        return

#------------------
class TestApp:
    def __init__(self, root):
        arm = None
        #arm = ArmTcp()
        #arm.connect(TEST_HOST, TEST_PORT)
        #arm.init('z1')
        #root.geometry("400x300")

        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.lTitle_ = tk.Label(frm, text = "Test")
        self.lTitle_.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.N,tk.S))

        #self.tipPanel = TipPanel(frm, arm)
        self.frm = frm

#-------------------------
#    main 
#-------------------------
root = tk.Tk()
app = TestApp(root)
root.mainloop()

