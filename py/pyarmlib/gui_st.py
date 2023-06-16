import tkinter as tk
from tkinter import ttk
from armLib import *
from utils import *
import threading

BORDER_W = 2
#----------
class StPanel(object):
    def __init__(self, topFrm, arm, N_joints):
        self.arm_ = arm
        self.N_joints = N_joints

        #----
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        self.label_joints_ = []
        for i in range(N_joints):
            lt = tk.Label(frm, borderwidth=BORDER_W, relief="solid", text = "J"+str(i+1))
            lv = tk.Label(frm, borderwidth=BORDER_W, relief="solid", text = "0.0")
            lt.grid(column=i, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
            lv.grid(column=i, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
            frm.columnconfigure(i, minsize=100)

        for i in range(2):
            frm.rowconfigure(i, minsize=50)

            self.label_joints_.append(lv)

        self.frm = frm
        return 

    #---
    def update(self):
        st = self.arm_.getSt()

        return

#------------------
class TestApp:
    def __init__(self, root):
        arm = Arm()
        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        lTitle = tk.Label(frm, borderwidth = BORDER_W, text = "Test")
        lTitle.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.pnl_ = StPanel(frm, arm, 6)
        self.pnl_.frm.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frm = frm

#----------
# main
#----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()