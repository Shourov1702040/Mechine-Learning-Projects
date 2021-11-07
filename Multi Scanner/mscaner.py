import numpy as np
import pandas as pd
import cv2, re, string,random,pymysql, pytesseract
import tkinter as tk
import pyperclip as pc
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pytesseract import image_to_string
from hashlib import sha256 as pyHash
from tkinter import filedialog 
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import TwoLineAvatarListItem,TwoLineAvatarIconListItem,ImageRightWidget
from kivymd.uix.list import MDList,IconLeftWidget,IconRightWidget,ImageLeftWidget
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.metrics import dp
from functools import partial
from kivy.core.window import Window
Window.size=(320,580)

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
conn = pymysql.connect(host="localhost", user="root", passwd="",db="test")
MyCursor = conn.cursor()

class LoginScreen(Screen): pass
class HomeScreen(Screen): pass
class ProfileScreen(Screen): pass
class Camera_screen(Screen): pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(Camera_screen(name='cam_scr'))

class PictureFloatLayout(FloatLayout):
    source = StringProperty()

#______________________________________ Main class _________________________________________
class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.borderless=True
        theme_colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'x']

        self.theme_cls.primary_palette="Blue"
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_hue="A700"
        self.screen = Builder.load_file('mscanner.kv')

        # Assumptions
        self.img_to_text_path = ''
    
    def build(self):
        return self.screen

    def login_fun(self):
        self.userId = self.screen.get_screen('login').ids.user_id.text
        self.userpass = self.screen.get_screen('login').ids.password_t.text

        self.userId = 'liakot@gmail.com'
        self.userpass = '121212'
        # self.userId = 'bruce@gmail.com'
        # self.userpass = '121212'

        hasher = pyHash()
        arrxd = bytes(self.userpass, 'utf-8')
        hasher.update(arrxd)
        password = hasher.hexdigest()

        sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
        MyCursor.execute(sql,self.userId)
        self.user_login_data = MyCursor.fetchone()
        closebtn = MDFlatButton(text='OK', on_release=self.close_dialog1)
        self.login_flag = 0
        if self.user_login_data and self.user_login_data[3]==password:
            self.login_flag = 1
            self.screen.get_screen('login').ids.user_id.text = ''
            self.screen.get_screen('login').ids.password_t.text = ''
            MDApp.get_running_app().root.current = "home"
            MDApp.get_running_app().root.transition.direction = 'left'
        else:
            self.screen.get_screen('login').ids.user_id.text = ''
            self.screen.get_screen('login').ids.password_t.text = ''
            self.dialog1 = MDDialog(title="Error",text='Invalid user email or password!\nTry again', size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog1.open()

    def close_dialog1(self,args): self.dialog1.dismiss()

    def set_values_after_login(self):
        if self.login_flag == 1:
            img_name = self.user_login_data[1].split('@')[0]
            imgpath = f"D:/Working_dir/Programming/Python/MultiScanner/User_images/{img_name}.jpg"
            self.screen.get_screen('home').ids.main_name_key.text = f"{self.user_login_data[0]}"
            self.screen.get_screen('home').ids.username_email.text = f"{self.user_login_data[1]}"
            self.screen.get_screen('home').ids.user_image.source = imgpath

            self.screen.get_screen('profile').ids.profile_img.source = imgpath
            self.screen.get_screen('profile').ids.profile_name.text = f"{self.user_login_data[0]}"
            self.screen.get_screen('profile').ids.profile_email.text = f"{self.user_login_data[1]}"

    # signup functions __________________________________________________________________
    def get_registration_values(self):
        name = self.screen.get_screen('login').ids.user_name_sign.text
        email = self.screen.get_screen('login').ids.user_email_sign.text
        img_path = self.screen.get_screen('login').ids.image_path_sign.text
        password = self.screen.get_screen('login').ids.password_sign.text
        password2 = self.screen.get_screen('login').ids.password_cnfm_sign.text

        self.all_value = None
        
        flag = 1
        erreo_text = ''  
        sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
        MyCursor.execute(sql,email)
        data2 = MyCursor.fetchone()

        if name=='' or email=='' or password==''or password2=='':
            flag=0
            erreo_text = 'Error!!!!!!\nPlease fill up all requirements.'

        elif password!=password2:
            flag=0
            erreo_text = 'Error!!!!!!\nType same password in both place.'
        elif len(password)<6 :
            flag=0
            erreo_text = 'Password is too weak\nMinimum password length 6, containing digits and special character'
        elif data2:
            flag=0
            erreo_text = 'Error!!!!!!\nThis email is already registered!!\nTry with other.'

        if flag==1:
            with open(img_path,'rb') as File_t:
                binary_img = File_t.read()
                img_path = binary_img

            hasher = pyHash()
            arr = bytes(password, 'utf-8')
            hasher.update(arr)
            password = hasher.hexdigest()

            self.all_value = (name,email,img_path,password)
            sql = "INSERT INTO `user_info` (`Name`, `Email`, `image`, `Password`) VALUES (%s,%s,%s,%s)"
            MyCursor.execute(sql,self.all_value)
            img_name_23 = email.split('@')[0]

            storeFilePth = f"D:/Working_dir/Programming/Python/MultiScanner/User_images/{img_name_23}.jpg"
            with open(storeFilePth,'wb') as img_write:
                img_write.write(binary_img)
                img_write.close()

            conn.commit()
            o_text = "Congratulation!!\nYour registration is complete\nLogin in your account"
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog2)
            self.dialog2 = MDDialog(title="Congratulation",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog2.open()

            self.screen.get_screen('login').ids.user_name_sign.text=''
            self.screen.get_screen('login').ids.user_email_sign.text=''
            self.screen.get_screen('login').ids.image_path_sign.text=''
            self.screen.get_screen('login').ids.password_sign.text=''
            self.screen.get_screen('login').ids.password_cnfm_sign.text=''
        else:
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog2)
            self.dialog2 = MDDialog(title="Error",text=erreo_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog2.open()

            self.screen.get_screen('login').ids.user_name_sign.text=''
            self.screen.get_screen('login').ids.user_email_sign.text=''
            self.screen.get_screen('login').ids.image_path_sign.text=''
            self.screen.get_screen('login').ids.password_sign.text=''
            self.screen.get_screen('login').ids.password_cnfm_sign.text=''

    def close_dialog2(self,args):
        self.dialog2.dismiss()

    def go_to_home(self):
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.transition.direction = 'right'

    def go_to_profile(self):
        MDApp.get_running_app().root.current = "profile"
        MDApp.get_running_app().root.transition.direction = 'left'

    def file_manager_open(self):
        root = tk.Tk()
        root.withdraw()
        path = str(filedialog.askopenfilename(title='Choose a file'))
        self.screen.get_screen('login').ids.image_path_sign.text = str(path)

    def logout_fun(self):
        MDApp.get_running_app().root.current = "login"
        MDApp.get_running_app().root.transition.direction = 'right'

    def file_manager_open2(self):
        root = tk.Tk()
        root.withdraw()
        self.img_to_text_path = str(filedialog.askopenfilename(title='Choose a file'))
        if self.img_to_text_path!='':
            self.screen.get_screen('home').ids.choose_to_load.text = 'Loaded'
            self.img_to_text()
        else:
            Snackbar(text='No image selected').open()

    def Show_img(self):
        from kivy.uix.image import Image
        if self.img_to_text_path!='':
            pop = Popup(title='Original image', content=Image(source=self.img_to_text_path), size_hint=(None, None), size=(345, 400))
            pop.open()
        else:
            Snackbar(text='No Image selected').open()
    def img_to_text(self):
        from PIL import Image
        img = Image.open(self.img_to_text_path)
        text_extracted = image_to_string(img)
        text_extracted = text_extracted[:-2]
        self.screen.get_screen('home').ids.text_extracted.text = text_extracted
        self.screen.get_screen('home').ids.text_extracted.hint_text = ''
        Snackbar(text='Image to text conversion successfully done').open()

    def copy_to_clipboard(self):
        text_to_copy = self.screen.get_screen('home').ids.text_extracted.text
        if text_to_copy!='':
            pc.copy(text_to_copy)
            Snackbar(text='Text coppied to clipboard').open()
        else:
            Snackbar(text='There is nothing to copy').open()

    def clear1(self):
        self.screen.get_screen('home').ids.text_extracted.text = ''
        self.screen.get_screen('home').ids.text_extracted.hint_text = 'Text'

    def open_camera(self):
        self.img_to_text_path = ''
        self.screen.get_screen('home').ids.choose_to_load.text = 'Choose'
        MDApp.get_running_app().root.current = "cam_scr"
        MDApp.get_running_app().root.transition.direction = 'left'
        self.capture = cv2.VideoCapture(0)
        self.capture.set(10,70)
        self.capture.set(10,75)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        
    def load_video(self, *args):
        ret, frame = self.capture.read()
        # frame = cv2.flip(frame,1)   # for mirror camera
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.screen.get_screen('cam_scr').ids.cam_box.texture = texture

    def save_image(self, *args):
        img_name = 'D:/Working_dir/Programming/Python/MultiScanner/CaptureImages/test1.png'
        cv2.imwrite(img_name, self.image_frame)
        self.go_to_home()
        self.img_to_text_path = img_name
        self.img_to_text()

    def paste_from_clipboard(self):
        text_to_paste = pc.paste()
        if text_to_paste!='':
            self.screen.get_screen('home').ids.text_to_speech.text = text_to_paste
            self.screen.get_screen('home').ids.text_to_speech.hint_text = ''
        else:
            Snackbar(text='Clipboard is empty').open()

    def copy_to_clipboard2(self):
        text_to_copy = self.screen.get_screen('home').ids.text_to_speech.text
        if text_to_copy!='':
            pc.copy(text_to_copy)
            Snackbar(text='Text coppied to clipboard').open()
        else:
            Snackbar(text='There is nothing to copy').open()

    def clear2(self):
        self.screen.get_screen('home').ids.text_to_speech.text = ''
        self.screen.get_screen('home').ids.text_to_speech.hint_text = 'Text'

    def text_to_speech_fun(self):
        import pyttsx3

        text_to_speech_t = self.screen.get_screen('home').ids.text_to_speech.text
        if text_to_speech_t!='':
            engine = pyttsx3.init()
            voices = list(engine.getProperty('voices'))
            engine. setProperty("rate", 150)
            engine.setProperty('voice', voices[1].id)
            engine.say(text_to_speech_t)
            engine.runAndWait() 
        else:
            Snackbar(text='There is nothing for speaking').open()

if __name__=='__main__':
    DemoApp().run()