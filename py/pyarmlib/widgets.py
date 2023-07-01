import tkinter as tk
import time
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from utils import *
import shlex, subprocess
from threading import Thread


BORDER_W = 2
STICKY_ALL = (tk.N, tk.S, tk.E, tk.W)
T_LOG_DELAY = 2.0

#----
class ConsolePanel(object):
    def __init__(self, topFrm, sTitle, sCmd):
        frm = ttk.Frame(topFrm, padding=(3,3,12,12))
       
        #---- title
        lt = tk.Label(frm, text = sTitle)
        lt.grid(row=0, column=0, sticky="news")

       
        tlog = ScrolledText(frm)
        tlog.grid(row=1, column = 0, pady = 10, sticky="news")
        tlog.tag_config('error', background="yellow", foreground="red")
        # dbg
        if False:
            s = "Run console cmd: '"+sCmd+"'..."
            for i in range(100):
                s = s + "log dbg line " + str(i) + "\n"
            tlog.insert(tk.INSERT, s)

        #----
        tlog.configure(state ='disabled')  # read only 
        self.tlog_ = tlog
        
        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=3)
        frm.columnconfigure(0, weight=1)

        self.frm  = frm
        
        #------
        #----
        thd = Thread(target=self.run_thd_,  daemon=True)
        thd.setDaemon(True)
        thd.start()
        self.run_thd_ = thd
        return

    
    #-----
    def run_thd_(self):
        #args = shlex.split(sCmd)
        #print("Run cmd:'" + sCmd + "'")
        with subprocess.Popen(["./tmp.sh"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True) as p:
            print("run_thd_() started...")
            #-----
            
            for s in p.stdout:
                print(s)
                self.tlog_.insert(tk.INSERT, s)
                time.sleep(0.2)  
            #-----
            while False:
                sOut, sErr = p.communicate()
                self.tlog_.insert(tk.INSERT, sOut)
                self.tlog_.insert(tk.INSERT, sErr, 'error')
                print("[dbg]---- sOut ----")
                print(sOut)
                print("[dbg]---- sErr ----")
                print(sErr)
                time.sleep(T_LOG_DELAY)

    
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
