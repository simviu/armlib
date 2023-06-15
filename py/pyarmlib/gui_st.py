import tkinter as tk
from tkinter import ttk
from armTcp import *
from utils import *
import threading


#----------
class StPanel:
    def __init__(self, topFrm, arm):
        self.arm_ = arm

        #----
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
        ln = tk.Label(frm, text = "joint"+str(idx+1))
        ls = tk.Label(frm, text = "q,qd,Torque")
        la = tk.Label(frm, text = "angle")

        bar=tk.Scrollbar(frm, orient='horizontal')
        #bar.set(0.30, 0.5)
        bar['command'] = self.scrollCbk

        ln.grid(row=1, column=0, sticky=(tk.E,tk.W))
        bar.grid(row=1, column=1, sticky=(tk.E,tk.W))
        ls.grid(row=0, column=2, sticky=(tk.E,tk.W))
        la.grid(row=0, column=1, sticky=(tk.E,tk.W))

        frm.columnconfigure(1, minsize=500)
        frm.rowconfigure(1, minsize=50)
        frm.grid(row=idx, column=0, sticky=(tk.N,tk.S,tk.W,tk.E))
        self.frm = frm

        self.bar = bar 
        self.frm = frm
        self.label_st = ls
        self.label_angle = la
        #----
        self.update()
        return
