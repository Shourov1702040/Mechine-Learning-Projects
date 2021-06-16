from tkinter.ttk import *
from tkinter import *
import time
from Classification import Classification

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


        item_info = ""
        if cata == "plants":
            if item_i == "Apple":
                item_info = "icon_image/trree_ap.png@Detect Apple plant disease@models/apple_plant_Model.p@#E40000"
            elif item_i == "Corn":
                item_info = "icon_image/corn_plant2.png@Detect Corn plant disease@models/corn_plant_Model.p@#22A61E"
            elif item_i == "Grape":
                item_info = "icon_image/grape_plant.JPG@Detect Grape plant disease@models/grape_plant_Model.p@#678623"
            elif item_i == "Cherry":
                item_info = "icon_image/cherry_plant.jpg@Detect Cherry Plant disease@models/cherry_plant_Model.p@#265909"
            elif item_i == "Pepper":
                item_info = "icon_image/peeper_plant.jpg@Detect Pepper plant disease@models/pepper_plant_Model.p@#b70000"
            elif item_i == "Potato":
                item_info = "icon_image/potato_plant1.png@Detect Potato plant disease@models/potato_plant_Model.p@#a67d00"
            elif item_i == "Tomato":
                item_info = "icon_image/tomato_plant.jpg@Detect Tomato plant disease@models/tomato_plant_Model.p@#620D0D"

        elif cata=='fruits':
            if item_i=="Apple":
                item_info = "icon_image/apple.jpg@Detect Apple Fruit disease@models/apple_fruit_Model.p@#E40000"
            elif item_i=="Banana":
                item_info = "icon_image/banana.jpg@Detect Banana Fruit disease@models/banana_fruit_Model.p@#ffef00"
            elif item_i=='Orange':
                item_info = "icon_image/orange.jpg@Detect Orange Fruit disease@models/orange_fruit_Model.p@#f76a04"

        classification_page = Classification(item_info)

        self.destroy()


