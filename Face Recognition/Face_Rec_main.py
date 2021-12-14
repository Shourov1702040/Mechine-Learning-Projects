"""
Delta electro code
Md Touhid Islam
Depertment of CSE, HSTU
https://www.facebook.com/Shourov40
"""

from tkinter import *
import tkinter.ttk as ttk
import cv2
from tkinter import messagebox
import numpy as np
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from PIL import Image, ImageTk
from progress import PSS

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

#_________________________________________ tab1 design _______________________________________________

        self.label11 = Label(self.tab1,text="Data Collection and Training",font=self.font1,bg="#ffa749")
        self.label11.pack(pady=20,anchor=CENTER)

        # self.label12 = Label(self.tab1,text="Enter your name ",font=self.font2,bg="#ffa749")
        # self.label12.place(x = 100, y = 130)

        # self.entry11 = Entry(self.tab1,font=self.font3)
        # self.entry11.place(x= 60, y = 180)

        img = Image.open(r"cad1.png")
        self.top_image = ImageTk.PhotoImage(img)

        self.top_image_label = Label(self.tab1, image=self.top_image, bg='#ffa749')
        self.top_image_label.place(x=330, y=90)

        self.label13 = Label(self.tab1, text="Number of image sample ", font=self.font2, bg="#ffa749")
        self.label13.place(x=60, y=250)

        self.spinvar = DoubleVar()
        self.spin1 = Spinbox(self.tab1, from_=100, to=1000, width=25, textvariabl=self.spinvar, font='arial 16 bold')
        self.spinvar.set(250)
        self.spin1.place(x=60, y=300)

        text2 = 'choose images directory'
        self.label4 = Label(self.tab1, text=text2, font='arial 16 bold', bg="#ffa749")
        self.label4.place(x=440, y=250)

        self.path = StringVar()
        self.path_entry = Entry(self.tab1, font=self.font3, textvariable=self.path, width=21)
        self.path_entry.place(x=440, y=300)

        self.save_btn = Button(self.tab1, text="open", font='arial 12 bold', command=self.model_loc)
        self.save_btn.place(x=698, y=299)


        self.label5 = Label(self.tab1, text="Start Capturing images sample ", font='arial 16 bold', bg="#ffa749")
        self.label5.place(x=260, y=380)

        self.capBtn = Button(self.tab1, text="Capture", font='arial 15 bold',bd=2,bg="#402c20",fg="#FFF",
                             command=self.cap_fun)
        self.capBtn.place(x=370, y=420)

        self.label6 = Label(self.tab1, text="Start Training process", font='arial 19 bold', bg="#ffa749")
        self.label6.place(x=155, y=530)

        self.start_btn = Button(self.tab1, text="START", font='arial 15 bold', bg="#000", fg="#ffa749", width=17
                               ,bd=3,command=self.training_fun)
        self.start_btn.place(x=440, y=530)



#_________________________________________ tab2 design _________________________________________________

        self.label21 = Label(self.tab2,text="Facial Recognition", font=self.font1,bg='#42bcf5')
        self.label21.pack(pady=20, anchor=CENTER)

        self.labe22 = Label(self.tab2, text="Enter your name", font='arial 17 bold', bg="#42bcf5")
        self.labe22.place(x=190, y=180)

        self.name_entry = Entry(self.tab2,font=self.font3)
        self.name_entry.place(x=390,y=180)

        self.labe22 = Label(self.tab2, text="Open camera and recognize your face", font='arial 16 bold', bg="#42bcf5")
        self.labe22.pack(pady=200,anchor=CENTER)

        self.butt = Button(self.tab2,text="Camera",font='Arial 50 bold',fg = "#249DCC",bg='#000',bd=5,width=15,
                           command=self.recognition_fun)
        self.butt.place(x=125,y=360)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Functions @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def face_extractor(self,img):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_classifier.detectMultiScale(self.gray, 1.3, 5)

        if self.faces == (): #if self.faces is ():
            return None

        for (x, y, w, h) in self.faces:
            self.cropped_face = img[y:y + h, x:x + w]
        return self.cropped_face

    def cap_fun(self):
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        self.count = 0

        if self.path_entry.get()!='':
            while True:
                self.ret, self.frame = cap.read()
                if self.face_extractor(self.frame) is not None:
                    self.count = self.count + 1
                    self.face = cv2.resize(self.face_extractor(self.frame), (400, 400))
                    self.face = cv2.cvtColor(self.face, cv2.COLOR_BGR2GRAY)

                    self.file_name_path = f'{self.path_entry.get()}/' + str(self.count) + '.jpg'
                    cv2.imwrite(self.file_name_path, self.face)

                    cv2.putText(self.face, str(self.count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face cropped', self.face)
                else:
                    pass
                if cv2.waitKey(1) == 13 or self.count==self.spinvar.get():
                    break
            cv2.destroyAllWindows()
            messagebox.showinfo("Done",f'Successfully collected {self.count} samples')
        else:
            messagebox.showerror('Error',"You haven't select any directory path")

    def training_fun(self):
        if self.path_entry.get()!='':
            self.data_path = f'{self.path_entry.get()}/'
            self.onlyfiles = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]

            self.Training_Data, self.Labels = [], []

            for i, file in enumerate(self.onlyfiles):
                self.image_path = self.data_path + self.onlyfiles[i]
                self.images = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
                self.Training_Data.append(np.asarray(self.images, dtype=np.uint8))
                self.Labels.append(i)
            self.Labels = np.asarray(self.Labels, dtype=np.int32)
            self.model = cv2.face.LBPHFaceRecognizer_create()
            self.model.train(np.asarray(self.Training_Data), np.asarray(self.Labels))
            # print("Training is complete")
            self.flag = True
            ss = PSS()
            messagebox.showinfo("Successful","Training completed successfully")
        else:
            messagebox.showerror('Error',"You haven't select any directory path")

    def recognition_fun(self):
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        if self.flag == False:
            messagebox.showerror("Training error",'You haven\'t train any model. Go to previous tab and train model')
        elif self.name_entry.get()!='' and self.flag==True:
            cap = cv2.VideoCapture(0)
            # cap.set(3, 640)
            # cap.set(4, 480)
            cap.set(10, 70)
            cap.set(10, 75)
            while True:
                ret, frame = cap.read()
                self.image, self.face = self.face_detector(frame)

                try:
                    face = cv2.cvtColor(self.face, cv2.COLOR_BGR2GRAY)
                    result = self.model.predict(face)

                    if result[1] < 500:
                        self.confidence = int(100 * (1 - (result[1]) / 300))
                        self.display_string = str(self.confidence) + "% confidence it is user"
                    cv2.putText(self.image, self.display_string, (60, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                    if self.confidence > 70:
                        cv2.putText(self.image, f"{self.name_entry.get()}", (120, 450), cv2.FONT_HERSHEY_COMPLEX, 3,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        cv2.imshow("Face cropper", self.image)
                    else:
                        cv2.putText(self.image, "Unknown", (120, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2,
                                    cv2.LINE_AA)
                        cv2.imshow("Face cropper", self.image)
                except:
                    cv2.putText(self.image, "Face not found", (50, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2,
                                cv2.LINE_AA)
                    cv2.imshow("Face cropper", self.image)
                    pass
                if cv2.waitKey(1) == 13:
                    break
            cap.release()
            cv2.destroyAllWindows()

        else:
            messagebox.showerror("Error","You haven't enter your name!!!!")

    def face_detector(self,img, size=0.5):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_classifier.detectMultiScale(self.gray, 1.3, 5)

        if self.faces == (): #if self.faces is ():
            return img, []

        for (x, y, w, h) in self.faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.roi = img[y:y + h, x:x + w]
            self.roi = cv2.resize(self.roi, (200, 200))
        return img, self.roi

    def model_loc(self):
        dir = filedialog.askdirectory()
        self.path.set(dir)

def main():
    root = Tk()
    app = FaceRecongition(root)
    root.title("Image to text")
    root.geometry("830x650+520+180")
    # root.resizable(False,False)
    root.mainloop()
if __name__ == '__main__':
    main()
