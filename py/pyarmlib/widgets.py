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
        #----
       
        tlog = ScrolledText(frm)
        tlog.grid(row=1, column = 0, pady = 10, sticky="news")
        tlog.tag_config('error', background="yellow", foreground="red")
        # dbg
        if True:
            s = "Run console cmd: '"+sCmd+"'..."
            for i in range(2):
                s = s + "log dbg line " + str(i) + "\n"
            tlog.insert(tk.INSERT, s)

        #----
        #tlog.configure(state ='disabled')  # read only 
        self.tlog_ = tlog
        #----
        #---- status bar
        ls = tk.Label(frm, text = "status")
        ls.grid(row=2, column=0, sticky="news")
        self.l_status_ = ls
        #----        
        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=3)
        frm.columnconfigure(0, weight=1)

        self.frm  = frm
        
        #------
        #----
        thd = Thread(target=self.run_bk_func_,  daemon=True)
        thd.setDaemon(True)
        thd.start()
        self.run_thd_ = thd
        return

    
    #-----
    def run_bk_func_(self):
        #args = shlex.split(sCmd)
        #print("Run cmd:'" + sCmd + "'")
        with subprocess.Popen(["./tmp.sh"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True) as p:
            print("run_thd_() started...")
            #-----

            while True:
                time.sleep(0.2)
                sout = p.stdout.readline()
                serr = p.stderr.readline()
                if p.poll() is not None:
                    break  
                #print(sout)
                #print(serr)          
                self.tlog_.insert(tk.INSERT, sout)
                self.tlog_.insert(tk.INSERT, serr, 'error')

            #for s in p.stdout:
            #    #print(str(s))
            #    self.tlog_.insert(tk.INSERT, s)

            

    
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
