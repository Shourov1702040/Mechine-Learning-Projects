from tkinter.ttk import *
from tkinter import *
import time

class PSS(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("720x150+570+370")
        self.config(bg="#FFF")
        self.title("Processing...")
        self.resizable(False, False)


        self.frame = Frame(self,height=150)
        self.frame.pack(fill=X)

        self.label0 = Label(self, text="Processing ", font="arial 15 bold")
        self.label0.place(x=280, y=5)

        self.label1 = Label(self, font="arial 15 bold")
        self.label1.place(x=400, y=5)

        self.s = Style()
        self.s.configure("TProgressbar", foreground="#0085b9", background="#0085b9", thickness=40)

        self.progress = Progressbar(self, style="TProgressbar", length=700, mode="determinate")
        self.progress.place(x=10, y=50)
        self.start()

    def start(self):

        for i in range(1, 101, 1):
            self.progress['value'] = i
            self.update_idletasks()
            self.label1.config(text=str(i) + "%")
            time.sleep(0.015)
        self.progress['value'] = 100
        self.destroy()


