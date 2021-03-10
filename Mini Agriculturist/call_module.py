from tkinter import *
import tkinter.ttk as ttk
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


class FaceRecongition(object):
    def __init__(self,master):
        self.master = master
        # self.master.config(bg="#ffa749")
        self.style = ttk.Style(master)
        self.style.configure('lefttab.TNotebook', background='#abc', tabposition='n')
        self.style.configure('.', font=('Helvetica', 15, 'bold'))

        self.tab_parent = ttk.Notebook(master, style='lefttab.TNotebook')
        self.tab1 = Frame(self.tab_parent, bg="#ffa749")
        self.tab2 = Frame(self.tab_parent, bg='#42bcf5')

        self.tab_parent.add(self.tab1, text=f'{"Train": ^28s}')
        self.tab_parent.add(self.tab2, text=f'{"Test": ^28s}')
        self.tab_parent.pack(expand=1, fill=BOTH)
        self.file = None

        self.font1 = 'arial 30 bold'
        self.font2 = 'arial 16 bold'
        self.font3 = 'Consolas 17 '

        self.flag = False

#_______________________________________________ tab1 design _________________________________________________________

        self.button = Button(self.tab1,text='test',font='arial 17 bold',command=self.test)
        self.button.pack(anchor=CENTER,pady=30)

        cam_img = PhotoImage(file=r'icon_image/cam.png')
        self.top_image = PhotoImage(file=r'icon_image/img.png')
        # self.button2 = Button(self.tab1, font='arial 17 bold',image = cam_img, compound=LEFT, command=self.test)
        # self.button2.pack(anchor=CENTER, pady=30)
        label = Label(self.tab1,image = self.top_image)
        label.pack()

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Functions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def test(self):
         asw = Banana_fruit_frame()



def main():
    root = Tk()
    app = FaceRecongition(root)
    root.title("Image to text")
    root.geometry("830x650+520+180")
    # root.resizable(False,False)
    root.mainloop()
if __name__ == '__main__':
    main()