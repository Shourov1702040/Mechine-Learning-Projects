from tkinter.ttk import *
from tkinter import *
import time
from apple_plant_frame import Apple_plant_frame
from corn_plant_frame import Corn_plant_frame
from grape_plant_frame import Grape_plant_frame
from cherry_plant_frame import Cherry_plant_frame
from pepper_plant_frame import Pepper_plant_frame
from potato_plant_frame import Potato_plant_frame
from apple_fruit_frame import Apple_fruit_frame
from tomato_plant_frame import Tomato_plant_frame
from banana_fruit_frame import Banana_fruit_frame
from orange_fruit_frame import Orange_fruit_frame

class PSS(Toplevel):
    def __init__(self,cata,item_i):
        Toplevel.__init__(self)
        self.geometry("720x150+620+350")
        self.config(bg="#FFF")
        self.title("Please wait...")
        self.resizable(False, False)


        self.frame = Frame(self,height=150)
        self.frame.pack(fill=X)

        self.label0 = Label(self, text="Loading", font="arial 15 bold")
        self.label0.place(x=300, y=5)

        self.label1 = Label(self, font="arial 15 bold")
        self.label1.place(x=400, y=5)

        self.s = Style()
        self.s.configure("TProgressbar", foreground="#0085b9", background="#0085b9", thickness=40)

        self.progress = Progressbar(self, style="TProgressbar", length=700, mode="determinate")
        self.progress.place(x=10, y=50)
        self.start(cata,item_i)

    def start(self,cata,item_i):

        for i in range(1, 101, 1):
            self.progress['value'] = i
            self.update_idletasks()
            self.label1.config(text=str(i) + "%")
            time.sleep(0.015)
        self.progress['value'] = 100

        if cata == "plants":
            if item_i == "Apple":
                apple_page = Apple_plant_frame()
            elif item_i == "Corn":
                corn_page = Corn_plant_frame()
            elif item_i == "Grape":
                grape_page = Grape_plant_frame()
            elif item_i == "Cherry":
                grape_page = Cherry_plant_frame()
            elif item_i == "Pepper":
                grape_page = Pepper_plant_frame()
            elif item_i == "Potato":
                grape_page = Potato_plant_frame()
            elif item_i == "Tomato":
                tomato_page = Tomato_plant_frame()

        elif cata=='fruits':
            if item_i=="Apple":
                appen_page= Apple_fruit_frame()
            elif item_i=="Banana":
                banana_page=Banana_fruit_frame()
            elif item_i=='Orange':
                orange_page = Orange_fruit_frame()
        self.destroy()


