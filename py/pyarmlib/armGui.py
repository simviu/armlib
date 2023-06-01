# Python program to demonstrate
# scale widget
import tkinter as tk
from tkinter import ttk
from armTcp import *
from utils import *
from threading import Thread

#---- def
SCROLL_DGR_UNITS = 1.0
SCROLL_DGR_PAGES = 10.0
SCROLL_BAR_W = 0.2

T_ST_THREAD = 0.2

#--- for test
TEST_HOST = "127.0.0.1"
TEST_PORT = 8192

#----------
class JointCtrl:
    def __init__(self, container, idx):
        #----
        self.angle = 0.0 # degree -180 to 180
        #----
        frm = ttk.Frame(container, padding=(3,3,12,12))
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

    
    #---- 
    def update(self):
        # angle
        self.label_angle.configure(text=str(self.angle))
        # bar
        f = self.angle /360.0 + 0.5
        df = SCROLL_BAR_W * 0.5
        self.bar.set(f-df, f+df)
        return
    
    #----
    def scrollCbk(self, act,d,step=None):
        a = self.angle 
        if act == tk.SCROLL:
            s = SCROLL_DGR_UNITS 
            if step == tk.PAGES:
                s = SCROLL_DGR_PAGES
            a = a + float(d) * s 

        elif act == tk.MOVETO:
            a = (float(d) - 0.5)*360
        else:
            raise("Error: unkown act:"+str(act))

        a = dgrIn180(a)
        self.angle = a

        self.update()
        return
        

#---------
class JointsPanel:
    def __init__(self, container, arm, N_joints):
        frm = ttk.Frame(container, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        #----
        self.jointCtrls = []
        for i in range(N_joints):
            jc = JointCtrl(frm, i)
            self.jointCtrls.append(jc)
        
        #-----
        self.frm  = frm
        self.arm_ = arm

        #---- st thread
        #print("start st thread...")
        #self.st_thread_ = Thread(self.func_get_st_(),  daemon=True)
        #self.st_thread_.start()
        #print("st thread running.")

        self.update()

        return
    
    #--
    def update(self):
        ok,st = self.arm_.getSt()
        if not ok:
            print("Error:wrong status")
            return
        
        angles = st.joints
        N = len(self.jointCtrls)
        for i in range(N):
            c = self.jointCtrls[i]
            c.angle = angles[i]
            c.update()
            
            return
    
    #--
    def func_get_st_(self):
        while True:
            print("func_get_st_() call...")
            #ok,st = self.arm_.getSt()
            time.sleep(T_ST_THREAD)
        return


#---------- test

def test():
    #h=Scrollbar(content, orient='horizontal')
    #h.set(0.30, 0.5)

    #s1 = Scale( root, variable = v1,
    #		from_ = 1, to = 100,
    #		orient = HORIZONTAL)
    #l2 = Label(content, text = "joint1")
    #l3 = Label(content, text = "Torque")

    #l2.grid(row=0, column=0, sticky=(E,W))
    #h.grid(row=0, column=1, sticky=(E,W))
    #l3.grid(row=0, column=2, sticky=(E,W))

    #b1 = Button(root, text ="Display Horizontal",
    #			command = show1,
    #			bg = "yellow")

    #l1 = Label(root)

    #root.columnconfigure(0, weight=1)
    #content.columnconfigure(0, weight=1)
    #content.columnconfigure(1, weight=5)
    #content.columnconfigure(2, weight=1)
    return

#------------------
class TestApp:
    def __init__(self, root):

        arm = ArmTcp()
        arm.connect(TEST_HOST, TEST_PORT)
        arm.init('z1')
        #self.root.geometry("400x300")

        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.jointsPanel = JointsPanel(frm, arm, 6)
        
        self.cmdInp = ttk.Entry(frm)
        self.cmdInp.grid(column=0, row=1, columnspan=1, sticky=(tk.S,tk.E,tk.W), pady=5, padx=5)

        self.frm = frm

#-------------------------
#    main 
#-------------------------
root = tk.Tk()
app = TestApp(root)
root.mainloop()

