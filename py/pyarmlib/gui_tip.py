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
    def __init__(self, container, arm, N_joints):
        frm = ttk.Frame(container, padding=(3,3,12,12))
        ss = ["+x", "-x", "+y", "-y", "+z", "-z"]

        #--- [row,col] grid pair
        grids=np.array([[2,2],[2,0], [1,1], [3,1], [1,4], [3,4]])
        btns = []
        for s in ss:
            b = tk.Button(frm, text ="+x", command=self.onButton)
            btns.append(b)
            b.grid(row=, column=, sticky=(E,W))

        return
    
    #----
    def onButton(self):
        print("button pressed")
        return

#---------------
# TipPanel
#---------------
class TipPanel():
    def __init__(self, container, arm, N_joints):
        frm = ttk.Frame(container, padding=(3,3,12,12))
        self.frm  = frm

        #----

        #-----
        self.arm_ = arm
        self.st_ = ArmSt()
        ok,self.st_ = self.arm_.getSt()
        if ok:
            self.update()
        else:
            print("Error:wrong status")

        return

#------------------
class TestApp:
    def __init__(self, root):

        #arm = ArmTcp()
        #arm.connect(TEST_HOST, TEST_PORT)
        #arm.init('z1')
        #self.root.geometry("400x300")

        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.tipPanel = TipPanel(frm, arm)
        
        
        self.frm = frm

#-------------------------
#    main 
#-------------------------
root = tk.Tk()
app = TestApp(root)
root.mainloop()

