import tkinter as tk
from tkinter import ttk
from utils import *

BORDER_W = 2

#----------
class StTipPanel(object):
    def __init__(self, topFrm):
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))


#----------
class StJointsPanel(object):
    def __init__(self, topFrm, N_joints):
        self.N_joints = N_joints

        #----
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        self.label_joints_ = []
        for i in range(N_joints):
            lt = tk.Label(frm, borderwidth=BORDER_W, relief="solid", text = "J"+str(i+1))
            lv = tk.Label(frm, borderwidth=BORDER_W, relief="solid", text = "0.0", fg='blue')
            lt.grid(column=i, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
            lv.grid(column=i, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
            self.label_joints_.append(lv)
            frm.columnconfigure(i, minsize=100)

        for i in range(2):
            frm.rowconfigure(i, minsize=50)

        self.frm = frm
        return 

    #---
    def set(self, joints):
        for i in range(self.N_joints):
            self.label_joints_[i].config(text=str(joints[i]))

        return

#------------------
class TestApp:
    def __init__(self, root):
        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        lTitle = tk.Label(frm, borderwidth = BORDER_W, text = "Test")
        lTitle.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.pnl_ = StJointsPanel(frm, 6)
        self.pnl_.frm.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frm = frm

        #---- set
        self.pnl_.set([10,20,30,40,50,60])

#----------
# main
#----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()