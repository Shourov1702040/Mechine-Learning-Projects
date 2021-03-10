from tkinter.ttk import *
from tkinter import *

class About(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('800x650+1000+200')
        self.title("Detect Corn disease")
        self.resizable(False, False)

        self.top = Frame(self,height=650,bg='#39393A')
        self.top.pack(fill=X)



