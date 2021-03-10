from tkinter.ttk import *
from tkinter import *
import datetime
from tkinter.font import Font
from tkinter import messagebox
from about_frame import About
from progress import PSS
from time import strftime

date = datetime.datetime.now().date()
date = str(date.strftime("%x"))

class Application(object):
    def __init__(self,master):
        self.master = master

        #frames create
        self.top = Frame(master,height=210,bg='#fff')
        self.top.pack(fill=X)
        self.bottom= Frame(master,height=490,bg='#09BF14')
        self.bottom.pack(fill=X)

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ top frame design  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.top_image = PhotoImage(file=r'icon_image/img.png')
        self.top_image_label = Label(self.top, image = self.top_image,bg='#fff')
        self.top_image_label.place(x=30,y=10)

        self.heading = Label(self.top, text='Mini Agriculturist', font='Arial 44 bold', bg='#fff',fg='#09AD1A')
        self.heading.place(x=250,y=50)

        self.top_image2 = PhotoImage(file=r'icon_image/apple_minitree.png')
        # self.top_image_label2 = Label(self.top, image=self.top_image2, bg='#fff')
        # self.top_image_label2.place(x=740, y=110)

        self.lbl = Label(self.top,font='Consolas 18 bold',fg="#000",bg="#fff")
        self.lbl.place(x=380,y=175)
        self.time()

        self.date_lbl=Label(self.bottom, text ='Date : '+date, font='Consolas 15 bold', fg='#000',bg='#09BF14')
        self.date_lbl.place(x=680,y=10)

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Bottom design @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.F_label = Label(self.bottom,text="Choose one item",font='Consolas 22 bold',bg="#09BF14",
                             fg="#fff")
        self.F_label.place(x=310,y=30)
        self.I_var = StringVar()
        self.F_checkBtn = Checkbutton(self.bottom,text='FRUITS ',variable=self.I_var,bg="#09BF14",
                                 onvalue="fruits",font='arial 17 bold')
        self.F_checkBtn.place(x=290,y=75)
        self.P_checkBtn = Checkbutton(self.bottom, text='PLANTS ', variable=self.I_var, bg="#09BF14",
                                 onvalue="plants", font='arial 17 bold',bd=2)
        self.P_checkBtn.place(x=450, y=75)

        self.I_var.initialize('plants')

        self.choose_f_label = Label(self.bottom,text='Choose a fruit name:',bg="#09BF14",font="arial 17 bold")
        self.choose_f_label.place(x=100,y=170)

        self.fruit_v = ['Apple','Banana','Orange','Guava','Pepe']
        self.F_cb= Combobox(self.bottom, values=self.fruit_v, font='Arial 15 bold',width=18,state='readonly')
        self.F_cb.set("select")
        self.F_cb.place(x=100,y=230)

        self.choose_p_label = Label(self.bottom, text='Choose a plant name:', bg="#09BF14",font="arial 17 bold")
        self.choose_p_label.place(x=530, y=170)

        self.plant_v = ["Apple","Cherry","Corn","Grape","Pepper","Potato","Tomato"]
        self.P_cb = Combobox(self.bottom, values=self.plant_v, font='Arial 17 bold',width=16,state='readonly')
        self.P_cb.set("select")
        self.P_cb.place(x=530, y=230)

        self.submit_label=Label(self.bottom,text="Submit your choise to justify",font='arial 17 bold',
                           bg="#09BF14")
        self.submit_label.place(x=260,y=330)

        self.submit_btn=Button(self.bottom,text="SUBMIT",font='Colsolas 20 bold',width=10,
                               fg="#09BF14",bg="#000",command=self.submit)
        self.submit_btn.place(x=310,y=400)

        self.clear_btn = Button(self.bottom,text='Clear',fg="#09BF14",bg="#000",font='Colsolas 12 bold'
                                ,command=self.clear_cb)
        self.clear_btn.place(x=383,y=230)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   menu portion   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.my_font = Font(family="Consolas", size=18, weight="bold")
        self.my_font2 = Font(family="Consolas", size=16, weight="bold")
        self.my_font3 = Font(family="Consolas", size=14, weight="bold")

        self.main_menu = Menu(master)
        master.config(menu=self.main_menu)

        self.fileMenu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.fileMenu, font=self.my_font3)

        self.editMenu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.editMenu, font=self.my_font3)
        self.aboutMenu = Menu(self.main_menu)
        self.main_menu.add_command(label="About",font=self.my_font3,command=self.about_fan)

        self.fileMenu.add_command(label="New", command=self.extraFun, font=self.my_font3)
        self.fileMenu.add_command(label="Search", font=self.my_font3)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Open", font=self.my_font3)

        self.saveMenu = Menu(self.fileMenu)
        self.saveMenu.add_command(label="Save", font=self.my_font3)
        self.saveMenu.add_command(label="Save as", font=self.my_font3)

        self.fileMenu.add_cascade(label="Save", menu=self.saveMenu, font=self.my_font3)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", font=self.my_font3)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ -x- Functions -x-  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def extraFun(self):
        print("jkb djb")
    def choose_item(self,cata,item_i):
        ps = PSS(cata,item_i)
    def submit(self):
        item = self.I_var.get()
        if item=="fruits":
            if self.F_cb.get()=="select" or self.F_cb.get()=="":
                messagebox.showerror("Error", "Select fruit item")
            else:
                fruit = self.F_cb.get()
                # print(item + ': ' + fruit)
                self.choose_item(item,fruit)
        elif item=="plants":
            if self.P_cb.get()=="select" or self.P_cb.get()=="":
                messagebox.showerror("Error", "Select plant item")
            else:
                plant = self.P_cb.get()
                print(item+": "+plant)
                self.choose_item(item, plant)
        else: messagebox.showwarning("Warning", "Haven't select category")

    def clear_cb(self):
        self.P_cb.set('select')
        self.F_cb.set('select')

    def time(self):
        string = strftime('%I:%M:%S %p')
        self.lbl.config(text=string)
        self.lbl.after(1000, self.time)

    def about_fan(self):
        about_page= About()



#-------------------------------------------------- Main frame ----------------------------------------------#
def main():
    root = Tk()
    app = Application(root)
    root.title("Mini Agriculturist")
    root.geometry("850x700+550+120")
    root.resizable(False,False)
    root.mainloop()
if __name__ == '__main__':
    main()
