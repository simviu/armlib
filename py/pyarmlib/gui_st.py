import tkinter as tk
from tkinter import ttk
from utils import *

BORDER_W = 2
STICKY_ALL = (tk.N, tk.S, tk.E, tk.W)

#----------
class VecPnl(object):
    def __init__(self, topFrm, sTitle, N, deci=2):
        self.labels_ = []
        self.deci_ = deci
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        lt = tk.Label(frm, text = sTitle, 
                      borderwidth=BORDER_W, relief="solid")
        lt.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frm.columnconfigure(0, minsize=100)

        #----
        for i in range(N):
            l = tk.Label(frm, text = "0",    
                        borderwidth=BORDER_W, 
                        relief="solid",
                        fg="blue")
            l.grid(column=i+1, row=0, sticky=STICKY_ALL)
            frm.columnconfigure(i+1, minsize=150)
            self.labels_.append(l)
        #----
        self.frm = frm

    #----
    def set(self, v):
        for i in range(len(self.labels_)):
            d = float(v[i])
            s = "%.2f" % d
            self.labels_[i].config(text = s)
        return 
    
#----------
class StTipPanel(object):
    def __init__(self, topFrm, sTitle):
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))

        lt = tk.Label(frm, text = sTitle, font=("Arial Bold", 12))
        lt.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frm.columnconfigure(0, minsize=200)

        p1 = VecPnl(frm, "Pos",   3)
        p2 = VecPnl(frm, "Euler", 3)
        p1.frm.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        p2.frm.grid(column=2, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.pnlPos_ = p1
        self.pnlEuler_ = p2
        self.frm = frm

    #---
    def set(self, T):
        self.pnlPos_.set(T.t)
        self.pnlEuler_.set(T.e)

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

        #-----
        lt = tk.Label(frm, borderwidth = BORDER_W, text = "Test")
        lt.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        #-----
        p1 = StJointsPanel(frm, 6)
        p1.frm.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        p1.set([10,20,30,40,50,60])

        #----
        p2 = StTipPanel(frm, "Tip")
        p2.frm.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        p2.set(Trans([1,2,3], [10,20,30]))
        
        #----
        self.frm = frm


#----------
# main
#----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()