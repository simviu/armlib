import tkinter as tk
import time
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from utils import *

BORDER_W = 2
STICKY_ALL = (tk.N, tk.S, tk.E, tk.W)

#----
class ConsolePanel(object):
    def __init__(self, topFrm, sTitle, sCmd):
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
       
        #---- title
        lt = tk.Label(frm, text = sTitle)
        lt.grid(row=0, column=0, sticky="news")

       
        tlog = ScrolledText(frm)
        tlog.grid(row=1, column = 0, pady = 10, sticky="news")
        # dbg
        if True:
            s = "Run console cmd: '"+sCmd+"'..."
            for i in range(100):
                s = s + "log dbg line " + str(i) + "\n"
            tlog.insert(tk.INSERT, s)

        #----
        tlog.configure(state ='disabled')  # read only 
        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=3)
        frm.columnconfigure(0, weight=1)

        self.frm  = frm


#------------------
class TestApp:
    def __init__(self, root):

        lt = tk.Label(root, text = "Widget Test",
                      font = ("Times New Roman", 25))
        lt.grid(row=0, column=0, sticky="news")

        sCmd = "ping www.yahoo.com"
        pnl = ConsolePanel(root, "Command Console", sCmd)
        pnl.frm.grid(row=1, column=0, sticky="news")

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=10)
        root.columnconfigure(0, weight=1)

#----------
# main
#----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()