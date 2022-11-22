from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import cv2
import pytesseract
from PIL import Image
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from progress import PSS
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Image_to_text(object):
    def __init__(self,master):
        self.master = master

        self.style = ttk.Style(master)
        self.style.configure('lefttab.TNotebook',background='#abc', tabposition='nw')
        self.style.configure('.', font=('Helvetica', 14, 'bold'))

        self.tab_parent = ttk.Notebook(master, style='lefttab.TNotebook')
        self.tab1 = Frame(self.tab_parent,bg='#FFF')
        self.tab2 = Frame(self.tab_parent,bg='#FFF')

        self.tab_parent.add(self.tab1, text=f'{"Tab-1": ^25s}')
        self.tab_parent.add(self.tab2, text=f'{"Tab-2": ^25s}')
        self.tab_parent.pack(expand=1, fill=BOTH)
        self.file = None

#______________________________________ tab-1 Design _____________________________________

        self.top = Frame(self.tab1, height=260, )
        self.top.pack(fill=X)
        self.bottom = Frame(self.tab1, height=490)
        self.bottom.pack(fill=X)

        label1 = Label(self.top,text=" Character Detection ",font='arial 39 bold',relief='solid')
        label1.place(x=170,y=15)
        label2 = Label(self.top,text="Choose an image to detect text",font='arial 18 bold')
        label2.place(x=29,y=120)

        self.entry_val = StringVar()
        self.path = ""
        self.path_entry = Entry(self.top, font='consolas 17 ', width=38, textvariable=self.entry_val, bd=2,bg="#ececec")
        self.path_entry.place(x=27, y=153)

        self.chooseBtn = Button(self.top, text="choose", font='consolas 14 bold', width=7, bd=3, command=self.get_file)
        self.chooseBtn.place(x=490, y=150)

        self.submit_btn = Button(self.top, text='Submit', font='consolas 17 bold', fg="#fff", bg="#36a2bb", width=12,bd=3,command = self.submit_fun)
        self.submit_btn.place(x=615, y=148)

        self.clear_button = Button(self.top, text='Clear', font='Consolas 17 bold', bg='#b90000', fg='#FFF',width=12,command=lambda: self.clear(0))
        self.clear_button.place(x=27, y=210)

        self.save_btn = Button(self.top,text="Save", font='Consolas 17 bold', bg='#441f11', fg='#FFF', width=12,command=lambda: self.save_fun(0))
        self.save_btn.place(x=617,y=210)

        scroll = Scrollbar(self.bottom)
        scroll.pack(side=RIGHT, fill=Y)
        self.text = Text(self.bottom, font='Consolas 25 ', wrap=WORD, padx=10, pady=10, bd=2,yscrollcommand=scroll.set,fg="#FFF", bg="#000")
        self.text.pack()
        scroll.config(command=self.text.yview)

    # __________________________________ tab-2 Design ___________________________________

        self.top1 = Frame(self.tab2, height=260)
        self.top1.pack(fill=X)
        self.bottom1 = Frame(self.tab2, height=490)
        self.bottom1.pack(fill=X)

        label11 = Label(self.top1, text="  Image to Text  ", font='arial 39 bold', relief='solid')
        label11.place(x=220, y=15)
        label21 = Label(self.top1, text="Choose an image to convert into text", font='arial 18 bold')
        label21.place(x=29, y=115)

        self.entry_val1 = StringVar()
        self.path1 = ""
        self.path_entry1 = Entry(self.top1, font='consolas 17 ', width=38, textvariable=self.entry_val1, bd=2,bg="#ececec")
        self.path_entry1.place(x=27, y=153)

        self.chooseBtn1 = Button(self.top1, text="choose", font='consolas 14 bold', width=7, bd=3, command=self.get_file1)
        self.chooseBtn1.place(x=490, y=150)

        self.submit_btn1 = Button(self.top1, text='Submit', font='consolas 17 bold', fg="#fff", bg="#36a2bb", width=12, bd=3, command=self.submit_fun1)
        self.submit_btn1.place(x=615, y=148)

        self.clear_button1 = Button(self.top1, text='clear all', font='Consolas 17 bold', bg='#b90000', fg='#FFF', width=12,command=lambda: self.clear(1))
        self.clear_button1.place(x=27, y=210)

        self.show = Button(self.top1, text='show image', font='Consolas 17 bold', bg='#32a61a', fg='#FFF', width=11, command=self.show_img)
        self.show.place(x=317, y=210)

        self.save_btn1 = Button(self.top1, text="Save", font='Consolas 17 bold', bg='#441f11', fg='#FFF', width=12, command=lambda: self.save_fun(1))
        self.save_btn1.place(x=617, y=210)

        scroll1 = Scrollbar(self.bottom1)
        scroll1.pack(side=RIGHT, fill=Y)
        self.text1 = Text(self.bottom1, font='Consolas 20 ', wrap=WORD, padx=10, pady=10, bd=2,yscrollcommand=scroll1.set, fg="#FFF", bg="#000")
        self.text1.pack()
        scroll1.config(command=self.text1.yview)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Functions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def get_file(self):
        dir = filedialog.askopenfilename(parent=self.master,title='Choose a file')
        self.path = str(dir)
        self.entry_val.set(self.path)
    def submit_fun(self):
        if self.path!='':
            img = cv2.imread(self.path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            text_got=''
            hImg, wImg, _ = img.shape
            boxes = pytesseract.image_to_boxes(img)
            for b in boxes.splitlines():
                # print(b)
                b = b.split(' ')
                # print(b[0], end=" ")
                text_got = text_got+str(b[0])+' '
                x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                
                cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
                cv2.putText(img, b[0], (x + 10, hImg - y + 55), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 255), 2)
            # img = cv2.resize(img, (int(img.shape[1])*2, int(img.shape[0])*2)) # make image bigger
            self.text.delete(1.0, END)
            ps = PSS()
            self.text.insert(INSERT,text_got)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showerror("Error", "You haven't select any image file yet.")

    def get_file1(self):
        dir = filedialog.askopenfilename(parent=self.master, title='Choose a file')
        self.path1 = str(dir)
        self.entry_val1.set(self.path1)

    def submit_fun1(self):
        if self.path1 != "":
            img1 = Image.open(self.path1)
            text_got = pytesseract.image_to_string(img1)
            # print(text)
            self.text1.delete(1.0, END)

            ps = PSS()
            self.text1.insert(INSERT, text_got)
        else:
            messagebox.showerror("Error","You haven't select any image file yet.")

    def show_img(self):
        if self.path1!='':
            img = cv2.imread(self.path1)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else: messagebox.showerror("Error", "You haven't elect any image file")

    def clear(self,x):
        if x==0:
            self.path_entry.delete(first=0, last=100)
            self.text.delete(1.0, END)
        elif x==1:
            self.path_entry1.delete(first=0, last=100)
            self.text1.delete(1.0, END)

    def save_fun(self,x):
        if self.file==None:
            if x==0:
                self.file = asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
                if self.file == "": self.file = None
                else:
                    self.file = open(self.file, "w")
                    self.file.write(self.text.get(1.0, END))
                    self.file.close()
            elif x==1:
                self.file = asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
                if self.file == "": self.file = None
                else:
                    self.file = open(self.file, "w")
                    self.file.write(self.text1.get(1.0, END))
                    self.file.close()
        self.file = None

def main():
    root = Tk()
    app = Image_to_text(root)
    root.title("Image to text")
    root.geometry("820x650+520+180")
    # root.resizable(False,False)
    root.mainloop()
if __name__ == '__main__':
    main()
