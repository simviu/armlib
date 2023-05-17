# Python program to demonstrate
# scale widget

from tkinter import *
from tkinter import ttk
from pyarmlib import armTcp

#----------
class JointCtrl:
    def __init__(self, container, idx):
        frm = ttk.Frame(container, padding=(3,3,12,12))
        ln = Label(frm, text = "joint"+str(idx+1))
        ls = Label(frm, text = "q,qd,Torque")
        bar=Scrollbar(frm, orient='horizontal')
        bar.set(0.30, 0.5)

        ln.grid(row=0, column=0, sticky=(E,W))
        bar.grid(row=0, column=1, sticky=(E,W))
        ls.grid(row=0, column=2, sticky=(E,W))

        frm.columnconfigure(1, minsize=300)
        frm.grid(row=idx, column=0, sticky=(N,S,W,E))
        self.frm = frm

#---------
class JointsPanel:
    def __init__(self, container):
        frm = ttk.Frame(container, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(N, S, E, W))

        
        self.joints = []
        for i in range(6):
            jc = JointCtrl(frm, i)
            self.joints.append(jc)
            
        self.frm = frm
        
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
class App:
    def __init__(self, root):


        #self.root.geometry("400x300")

        frm = ttk.Frame(root, padding=(3,3,12,12))
        frm.grid(column=0, row=0, sticky=(N, S, E, W))

        self.jointsPanel = JointsPanel(frm)
        
        self.cmdInp = ttk.Entry(frm)
        self.cmdInp.grid(column=0, row=1, columnspan=1, sticky=(S,E,W), pady=5, padx=5)

        self.frm = frm

#-------------------------
#    main 
#-------------------------
root = Tk()
app = App(root)
root.mainloop()

