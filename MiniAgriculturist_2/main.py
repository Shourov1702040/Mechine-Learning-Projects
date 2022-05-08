import numpy as np
import pandas as pd
import cv2, pickle, re, string,random,pymysql,time,threading,datetime,webbrowser
import tkinter as tk
import urllib.request as urec
from smtplib import SMTP
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from hashlib import sha256 as pyHash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import filedialog 
from decimal import Decimal
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem,TwoLineAvatarIconListItem,ImageRightWidget
from kivymd.uix.list import MDList,IconLeftWidget,IconRightWidget,ImageLeftWidget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.metrics import dp
from functools import partial
from kivy.core.window import Window
Window.size=(347,620)
Window.top=54
Window.left=860

conn = pymysql.connect(host="localhost", user="root", passwd="",db="mini_agriculturist")
MyCursor = conn.cursor()

class LoginScreen(Screen): pass
class HomeScreen(Screen): pass
class ProfileScreen(Screen): pass
class ForgotPassScreen(Screen): pass
class AcctiveACountScreen(Screen): pass
class Change_password(Screen): pass
class Settings_screen(Screen): pass
class User_messenger(Screen): pass
class Admin_control(Screen): pass
class ADD_show_diease(Screen): pass
class Camera_screen(Screen): pass

# extra class for proper date picker option
class MyTextInput(MDTextField):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.text = ""
            return True
        return super(MyTextInput, self).on_touch_down(touch)

class PictureFloatLayout(FloatLayout):
    source = StringProperty()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(ForgotPassScreen(name='forgot_pass'))
sm.add_widget(Change_password(name='change_pass'))
sm.add_widget(AcctiveACountScreen(name='active_account'))
sm.add_widget(Settings_screen(name='settings_scr'))
sm.add_widget(User_messenger(name='user_message'))
sm.add_widget(Admin_control(name='admin_control'))
sm.add_widget(ADD_show_diease(name='Add_show_diease'))
sm.add_widget(Camera_screen(name='cam_scr'))


#______________________________________ Main class _________________________________________
class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.borderless=True
        # themes = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray'] 
        self.theme_cls.primary_palette="DeepPurple"
        self.theme_cls.theme_style="Light"
        # self.theme_cls.primary_hue="A400"
        self.screen = Builder.load_file('main.kv')
        
        item_names = ['Settings','Logout','Exit']
        self.menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in item_names
        ]
        self.menu_1 = MDDropdownMenu(
            caller=self.screen.get_screen('home').ids.commontoolbar,
            items=self.menu_items,
            width_mult=2,
        )

        self.menu_2 = MDDropdownMenu(
            caller=self.screen.get_screen('profile').ids.commontoolbar2,
            items=self.menu_items,
            width_mult=2,
        )

        # menu 3 ----
        item_names2 = ['Apple','Corn','Grape','Tomato']
        self.menu_items2 = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in item_names2
        ]
        self.menu_3 = MDDropdownMenu(
            caller=self.screen.get_screen('home').ids.drop_item,
            items=self.menu_items2,
            width_mult=2,
        )

        # messanger_options menu 4 -----
        item_names3 = ['View profile','Delete','Home','Exit']
        self.menu_items3 = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in item_names3
        ]
        self.menu_4 = MDDropdownMenu(
            caller=self.screen.get_screen('user_message').ids.messager_to,
            items=self.menu_items3,
            width_mult=2,
        )

        # menu 5 -------
        item_names4 = ['Uncheck','Delete','Home','Exit']
        self.menu_items4 = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback2(x),
            } for i in item_names4
        ]
        self.menu_5 = MDDropdownMenu(
            caller=self.screen.get_screen('admin_control').ids.admin_control_menu,
            items=self.menu_items4,
            width_mult=2.0,
        )

        # menu 6 -------
        item_names5 = ['Choose','Scaner']
        icons_5 = ['folder-multiple-image','credit-card-scan']
        self.menu_items5 = [
            {
                "text": item_names5[i],
                "viewclass": "IconListItem",
                "height": dp(40),
                "on_release": lambda x=item_names5[i]: self.menu_callback2(x),
                "icon":icons_5[i],
            } for i in range(2)
        ]
        self.menu_6 = MDDropdownMenu(
            caller=self.screen.get_screen('home').ids.suspect_img_choose_btn,
            items=self.menu_items5,
            width_mult=2.4,
        )

        #all empty assumptions------------------------------------
        self.suspect_img=''
        self.suspect_values=[]
        self.user_login_data=[]
        self.ck_delete_list=[]
        self.night_monkey_data=[]
        self.temp_flag_001 = ''
        self.b_user_info_020 = ''
        self.b_subadmin_info_020 = ''
        self.num_of_cap_image939 = 0

    def messanger_options(self):
        if self.user_login_data[5]==2:
            self.menu_4.open()

    def menu_callback(self, text_item):
        # print(text_item)
        if text_item=='Settings': self.go_to_settings()
        elif text_item=='Logout': 
            MDApp.get_running_app().root.current = "login"
            MDApp.get_running_app().root.transition.direction = 'right'
        elif text_item=='Home': 
            MDApp.get_running_app().root.current = "home"
            MDApp.get_running_app().root.transition.direction = 'right'
        elif text_item=='View profile': self.view_profile()

        elif text_item=='Delete': self.stop()
        elif text_item=='Exit': 
            self.root_window.close()

        else: 
            self.screen.get_screen('home').ids.drop_item.text = text_item
            self.screen.get_screen('home').ids.disease_name.text = 'Calculating.....'
            # self.screen.get_screen('home').ids.probability.text = 'Calculating.....'

        self.menu_1.dismiss()
        self.menu_2.dismiss()
        self.menu_3.dismiss()
        self.menu_4.dismiss()
        

    def menu_callback2(self,text_item):
        if text_item=='Delete': 
            self.delete_msg_call()
            self.admin_message_show()
        elif text_item=='Uncheck': 
            self.admin_message_show()
        elif text_item=='Home': 
            MDApp.get_running_app().root.current = "home"
            MDApp.get_running_app().root.transition.direction = 'right'
        elif text_item=='Choose':
            self.menu_6.dismiss()
            self.choose_suspect_img()
        elif text_item=='Scaner': 
            self.menu_6.dismiss()
            self.go_to_camera()
        elif text_item=='Exit': 
            self.root_window.close()

        self.menu_5.dismiss()
        

    def build(self):
        return self.screen
    
    #___________________ Login functions __________________________________________________
    def login_fun(self):
        self.userId = self.screen.get_screen('login').ids.user_id.text
        self.userpass = self.screen.get_screen('login').ids.password_t.text
        # self.userId = 'amber@gmail.com'
        # self.userpass = '1234@a'

        # self.userId = 'liakot@gmail.com'
        # self.userpass = '1234@a'
        # self.userId = 's@gmail

        hasher = pyHash()
        arrxd = bytes(self.userpass, 'utf-8')
        hasher.update(arrxd)
        password = hasher.hexdigest()

        sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
        MyCursor.execute(sql,self.userId)
        self.user_login_data = MyCursor.fetchone()
        closebtn = MDFlatButton(text='OK', on_release=self.close_dialog1)
        self.login_flag = 0
        # if not self.check_connection():
        #     self.screen.get_screen('login').ids.user_id.text = ''
        #     self.screen.get_screen('login').ids.password_t.text = ''
        #     self.dialog1 = MDDialog(title="Error",text='No internet!!!\nTry again', size_hint=(0.8,0.5), buttons=[closebtn])
        #     self.dialog1.open()
        if self.user_login_data and self.user_login_data[4]==password:
            self.login_flag = 1
            self.screen.get_screen('login').ids.user_id.text = ''
            self.screen.get_screen('login').ids.password_t.text = ''
            MDApp.get_running_app().root.current = "home"
            MDApp.get_running_app().root.transition.direction = 'right'
        else:
            self.screen.get_screen('login').ids.user_id.text = ''
            self.screen.get_screen('login').ids.password_t.text = ''
            self.dialog1 = MDDialog(title="Error",text='Invalid user email or password!\nTry again', size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog1.open()

    def close_dialog1(self,args): self.dialog1.dismiss()

    def set_values_after_login(self):
        if self.login_flag == 1:
            img_name = self.user_login_data[1].split('@')[0]
            imgpath = f"D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name}.jpg"
            self.screen.get_screen('home').ids.main_name_key.text = f"{self.user_login_data[0]}"
            self.screen.get_screen('home').ids.username_email.text = f"{self.user_login_data[1]}"
            self.screen.get_screen('home').ids.user_image.source = imgpath

            if self.user_login_data[5]==2:
                self.screen.get_screen('home').ids.control_panel.text = 'Admin panel'
                self.screen.get_screen('home').ids.control_msg.icon='account-cog'
            elif self.user_login_data[5]==0:
                self.check_user_new_msg()
                
    def check_user_new_msg(self):
        sql2 = "SELECT COUNT(*) FROM message WHERE `Email` = %s and `Sender`=%s and status=0"
        MyCursor.execute(sql2,(self.user_login_data[1],'Admin'))
        data2 = MyCursor.fetchall()
        data2 = [x for tupl in data2 for x in tupl]
        if data2[0]!=0:
            self.screen.get_screen('home').ids.control_panel.text = f"Message ({data2[0]} new)" 
        else: self.screen.get_screen('home').ids.control_panel.text = f"Message" 
            
    #___________________ signup functions __________________________________________________
    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save = self.on_save)
        date_picker.open()

    def on_save(self, instance, value, date_range):
        self.screen.get_screen('login').ids.date_sign.text=str(value)
        self.screen.get_screen('login').ids.date_sign.hint_text='Date of birth'

    def file_manager_open(self):
        root = tk.Tk()
        root.withdraw()
        path = str(filedialog.askopenfilename(title='Choose a file'))
        self.screen.get_screen('login').ids.image_path_sign.text = str(path)
        # print(self.ids.image_path_sign.text)

    def get_registration_values(self):
        name = self.screen.get_screen('login').ids.user_name_sign.text
        email = self.screen.get_screen('login').ids.user_email_sign.text
        img_path = self.screen.get_screen('login').ids.image_path_sign.text
        Dob = self.screen.get_screen('login').ids.date_sign.text
        password = self.screen.get_screen('login').ids.password_sign.text
        password2 = self.screen.get_screen('login').ids.password_cnfm_sign.text

        self.all_value = None
        
        flag = 1
        erreo_text = ''  
        sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
        MyCursor.execute(sql,email)
        data2 = MyCursor.fetchone()
        regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')

        if name=='' or email=='' or Dob=='' or password==''or password2=='' or img_path=='':
            flag=0
            erreo_text = 'Error!!!!!!\nPlease fill up all requirements.'

        elif not email.endswith('@gmail.com') and email[0].isalnum():
            flag=0
            erreo_text = 'Enter correct email'

        elif data2:
            flag=0
            erreo_text = 'Error!!!!!!\nThis email is already registered!!\nTry with other.'

        elif password!=password2:
            flag=0
            erreo_text = 'Error!!!!!!\nType same password in both place.'
        elif len(password)<6 or not any(i.isdigit() for i in password) or regex.search(password)==None:
            flag=0
            erreo_text = 'Password is too weak\nMinimum password length 6'

        elif not any(i.isupper() for i in password) and not any(i.islower() for i in password) :
            flag=0
            erreo_text = 'Password is too weak2\nUse uppercase or lower case character'

        if flag==1:
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
            self.all_value = [name,email,img_path,Dob,password,token]
            print(token)
            self.send_mail([email,name,token])
            self.screen.get_screen('login').ids.user_name_sign.text=''
            self.screen.get_screen('login').ids.user_email_sign.text=''
            self.screen.get_screen('login').ids.image_path_sign.text=''
            self.screen.get_screen('login').ids.date_sign.text=''
            self.screen.get_screen('login').ids.password_sign.text=''
            self.screen.get_screen('login').ids.password_cnfm_sign.text=''

            MDApp.get_running_app().root.current = "active_account"
        else:
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog2)
            self.dialog2 = MDDialog(title="Error",text=erreo_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog2.open()

    def close_dialog2(self,args):
        self.dialog2.dismiss()

    def activate_account_fun(self):
        token_user_in = self.screen.get_screen('active_account').ids.six_digit_code.text
        values = self.all_value
        token_original = values[5]

        with open(values[2],'rb') as File_t:
            binary_img = File_t.read()
            values[2] = binary_img

        hasher = pyHash()
        arr = bytes(values[4], 'utf-8')
        hasher.update(arr)
        password = hasher.hexdigest()
        values[4] = password

        values[5]=0

        values = tuple(values)
        sql = "INSERT INTO `user_info` (`Name`, `Email`, `image`, `DOB`, `Password`, `Status`,`facebook`,`github`) VALUES (%s,%s,%s,%s,%s,%s,'','')"
        if token_user_in==token_original:
            try:
                MyCursor.execute(sql,values)
                img_name_23 = values[1].split('@')[0]
                storeFilePth = f"D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name_23}.jpg"
                with open(storeFilePth,'wb') as img_write:
                    img_write.write(values[2])
                    img_write.close()

                conn.commit()
                o_text = "Congratulation!!\nYour registration is complete\nLogin in your account"
                closebtn = MDFlatButton(text='OK', on_release=self.close_dialog)
                self.dialog = MDDialog(title="Congratulation",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog.open()
                self.screen.get_screen('active_account').ids.six_digit_code.text=''
                self.logout_fun()
            except pymysql.Error as err:
                # print("---------------ERROR-----------------")
                print(err)
                o_text = "Invalid data !!!\nTry to provide correct data"
                closebtn = MDFlatButton(text='OK', on_release=self.close_dialog)
                self.screen.get_screen('active_account').ids.six_digit_code.text=''
                self.dialog = MDDialog(title="Error",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog.open()

        else:
            o_text = "Invalid code !!!\nEnter valid code"
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog)
            self.dialog = MDDialog(title="Error",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.screen.get_screen('active_account').ids.six_digit_code.text=''
            self.dialog.open()

    def close_dialog(self,args):
        self.dialog.dismiss()

    def send_mail(self,info):
        print(info)
        send_to_mail = info[0]
        me = "shourovcse17@gmail.com"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Mini Agriculturist: Conformation code"
        msg['From'] = "shourovcse17@gmail.com"
        msg['To'] = send_to_mail        
        html = f"""\
        <html>
        <head></head>
        <body>
            <p style="font-size:17px">Hello<br>
                Mr/Mrs. {info[1]}<br>
                Here is the 6 character conformation code.<br>
                Copy the code and enter in the application.
            </p>
            <h3>Code:</h3>
            <h1>{info[2]}</h1>
        </body>
        </html>
        """
        text_body = MIMEText(html, 'html')
        try:
            msg.attach(text_body)
            mail = SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login( "shourovcse17@gmail.com", '1112704646@gmail')
            mail.sendmail(me, send_to_mail, msg.as_string())
            mail.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")


    #___________________ Common functions _____________________________________________________

    def flip(self):
        self.screen.get_screen('login').ids.user_id.text = ''
        self.screen.get_screen('login').ids.password_t.text = ''
        self.screen.get_screen('login').ids.user_name_sign.text=''
        self.screen.get_screen('login').ids.user_email_sign.text=''
        self.screen.get_screen('login').ids.image_path_sign.text=''
        self.screen.get_screen('login').ids.date_sign.text=''
        self.screen.get_screen('login').ids.password_sign.text=''
        self.screen.get_screen('login').ids.password_cnfm_sign.text=''

    def option_fun(self): print("Pressed options 3 dots")

    def go_to_profile(self):
        self.night_monkey_data = [self.user_login_data[1],self.user_login_data[0]]
        img_name = self.user_login_data[1].split('@')[0]
        imgpath = f"D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name}.jpg"

        self.screen.get_screen('profile').ids.profile_picture.source = imgpath
        self.screen.get_screen('profile').ids.profile_name.text = self.user_login_data[0]
        # self.screen.get_screen('profile').ids.profile_email.text = self.user_login_data[1]

        self.screen.get_screen('profile').ids.profile_name_2.text = "Name:            "+str(self.user_login_data[0])
        self.screen.get_screen('profile').ids.profile_email_2.text = "Email:            "+str(self.user_login_data[1])
        self.screen.get_screen('profile').ids.profile_dob_2.text = "Date of birth:   "+str(self.user_login_data[3])
        i = int(self.user_login_data[5])
        status = ['Basic user','Sub-admin','Admin']
        self.screen.get_screen('profile').ids.profile_status_2.text = "Status:           "+str(status[i])

        MDApp.get_running_app().root.current = "profile"
        MDApp.get_running_app().root.transition.direction = 'left'

    def view_profile(self):
        values=[]
        if self.night_monkey_data:
            sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
            MyCursor.execute(sql,self.night_monkey_data[0])
            values =  MyCursor.fetchone()

        img_name = values[1].split('@')[0]
        imgpath = f"D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name}.jpg"

        self.screen.get_screen('profile').ids.profile_picture.source = imgpath
        self.screen.get_screen('profile').ids.profile_name.text = values[0]
        # self.screen.get_screen('profile').ids.profile_email.text = values[1]

        self.screen.get_screen('profile').ids.profile_name_2.text = "Name:            "+str(values[0])
        self.screen.get_screen('profile').ids.profile_email_2.text = "Email:            "+str(values[1])
        self.screen.get_screen('profile').ids.profile_dob_2.text = "Date of birth:   "+str(values[3])
        i = int(values[5])
        status = ['Basic user','Sub-admin','Admin']
        self.screen.get_screen('profile').ids.profile_status_2.text = "Status:           "+str(status[i])

        MDApp.get_running_app().root.current = "profile"
        MDApp.get_running_app().root.transition.direction = 'left'

    def see_facebook_web(self):
        if self.night_monkey_data:
            if self.night_monkey_data[0]!=self.user_login_data[1]:
                sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
                MyCursor.execute(sql,(self.night_monkey_data[0]))
                sstt = MyCursor.fetchone()
                link=sstt[6]
            else: link = self.user_login_data[6]
        else: link = self.user_login_data[6]
        if link!='':
            webbrowser.open(link)
        else:
            Snackbar(text='User hasn\'t added facebook account').open()

    def see_github_web(self):
        if self.night_monkey_data:
            if self.night_monkey_data[0]!=self.user_login_data[1]:
                sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
                MyCursor.execute(sql,(self.night_monkey_data[0]))
                sstt = MyCursor.fetchone()
                link=sstt[7]
            else: link = self.user_login_data[7]
        else: link = self.user_login_data[7]
        if link!='':
            webbrowser.open(link)
        else:
            Snackbar(text='User hasn\'t added Github account').open()

    def go_to_home(self):
        if self.user_login_data[5]==0:
            self.check_user_new_msg() 
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.transition.direction = 'right'
    def logout_fun(self): 
        MDApp.get_running_app().root.current = "login"
        MDApp.get_running_app().root.transition.direction = 'right'
    def pass_recover(self): 
        MDApp.get_running_app().root.current = "forgot_pass"
        MDApp.get_running_app().root.transition.direction = 'left' 

    def goto_change_pass(self): 
        forgot_user_mail = self.screen.get_screen('forgot_pass').ids.forgot_mail_id.text
        erreo_text = ''  
        sql = "SELECT * FROM `user_info` WHERE `Email` = %s"
        MyCursor.execute(sql,forgot_user_mail)
        data3 = MyCursor.fetchone()

        if data3:
            for_cnfm_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
            # print(for_cnfm_code)
            self.send_mail([data3[1],data3[0],for_cnfm_code])
            
            self.change_user_identity = [forgot_user_mail,for_cnfm_code]
            MDApp.get_running_app().root.current = "change_pass"
            MDApp.get_running_app().root.transition.direction = 'left'
            self.screen.get_screen('forgot_pass').ids.forgot_mail_id.text=''
        else:
            o_text = "This email hasn't an account!!!\nEnter valid email"
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog3)
            self.dialog3 = MDDialog(title="Error",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog3.open()
            self.screen.get_screen('forgot_pass').ids.forgot_mail_id.text=''
    def close_dialog3(self,args): self.dialog3.dismiss()

    def password_change_fun(self):
        user_cnmf_code = self.screen.get_screen('change_pass').ids.user_cnmf_code_id.text
        password1 = self.screen.get_screen('change_pass').ids.new_password.text
        password2 = self.screen.get_screen('change_pass').ids.new_password_2.text

        if user_cnmf_code==self.change_user_identity[1] and password1==password2:
            hasher = pyHash()
            arrxd = bytes(password1, 'utf-8')
            hasher.update(arrxd)
            password_xx = hasher.hexdigest()

            sql = "UPDATE `user_info` SET `Password` = %s WHERE `user_info`.`Email` = %s"
            MyCursor.execute(sql, (password_xx, self.change_user_identity[0]))
            conn.commit()

            self.screen.get_screen('change_pass').ids.user_cnmf_code_id.text=''
            self.screen.get_screen('change_pass').ids.new_password.text=''
            self.screen.get_screen('change_pass').ids.new_password_2.text=''

            o_text = "Successfully updated password!\nYou can login with new password"
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog4)
            self.dialog4 = MDDialog(title="Successful",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog4.open()
            MDApp.get_running_app().root.current = "login"
            MDApp.get_running_app().root.transition.direction = 'right'
        else:
            o_text = "Invalid conformaton code!\nOr passwords are not same\nTry again."
            closebtn = MDFlatButton(text='OK', on_release=self.close_dialog4)
            self.dialog4 = MDDialog(title="Error",text=o_text, size_hint=(0.8,0.5), buttons=[closebtn])
            self.dialog4.open()

            self.screen.get_screen('change_pass').ids.user_cnmf_code_id.text=''
            self.screen.get_screen('change_pass').ids.new_password.text=''
            self.screen.get_screen('change_pass').ids.new_password_2.text=''

    def close_dialog4(self,args):
        self.dialog4.dismiss()

    def got_to_recov(self): 
        MDApp.get_running_app().root.current = "forgot_pass"
        MDApp.get_running_app().root.transition.direction = 'right'

    def go_to_settings(self):
        self.screen.get_screen('settings_scr').ids.setting_face.text=''
        self.screen.get_screen('settings_scr').ids.setting_git.text=''

        img_name = self.user_login_data[1].split('@')[0]
        imgpath = f"D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name}.jpg"
        self.screen.get_screen('settings_scr').ids.setting_img.source=imgpath
        self.screen.get_screen('settings_scr').ids.setting_name.text=self.user_login_data[0]
        self.screen.get_screen('settings_scr').ids.setting_email.text=self.user_login_data[1]
        self.screen.get_screen('settings_scr').ids.setting_dob.text=str(self.user_login_data[3])
        self.screen.get_screen('settings_scr').ids.setting_face.text=self.user_login_data[6]
        self.screen.get_screen('settings_scr').ids.setting_git.text=self.user_login_data[7]
        MDApp.get_running_app().root.current = "settings_scr"
        MDApp.get_running_app().root.transition.direction = 'right'

    #___________________Feature page functions ___________________________________________________
    def choose_suspect_img(self):
        category_select = str(self.screen.get_screen('home').ids.drop_item.text)
        root = tk.Tk()
        root.withdraw()
        path = str(filedialog.askopenfilename(title='Choose a file'))

        if path!='' and category_select!='Category':
            type_cata = category_select+' plant'
            models_name = {'Apple plant':'apple.p','Corn plant':'corn.p','Grape':'grape.p'}
            model_n = models_name[type_cata]
            final_model_n = "D:/Working_dir/Programming/Python/Mini_Agriculturist-2/models/"+str(model_n)
            self.screen.get_screen('home').ids.suspect_img_choose_btn.text = 'Loaded'
            self.suspect_values = [type_cata,final_model_n,path]
            self.suspect_img = str(path)
            self.classify_disease()
        elif path=='': Snackbar(text='You haven\'t selected any image.' ).open()
        else: Snackbar(text='Select s category then choose an image.' ).open()

    def go_to_camera(self):
        MDApp.get_running_app().root.current = "cam_scr"
        MDApp.get_running_app().root.transition.direction = 'left'
        # self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(10,70)
        self.capture.set(10,75)
        Clock.schedule_interval(self.load_video, 1.0/30.0)

    def load_video(self, *args):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame,1)   # for mirror camera
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.screen.get_screen('cam_scr').ids.cam_box.texture = texture
        
    def save_image(self, *args):
        self.num_of_cap_image939 +=1
        img_name = f'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/Capture_images/cap_img{self.num_of_cap_image939}.png'
        cv2.imwrite(img_name, self.image_frame)
        category_select = self.screen.get_screen('home').ids.drop_item.text
        # Snackbar(text='Image successfully captured').open()
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.transition.direction = 'right'
        if category_select!='Category':
            type_cata = category_select+' plant'
            models_name = {'Apple plant':'apple.p','Corn plant':'corn.p','Grape':'grape.p'}
            model_n = models_name[type_cata]
            final_model_n = "D:/Working_dir/Programming/Python/Mini_Agriculturist-2/models/"+str(model_n)
            
            self.screen.get_screen('home').ids.suspect_img_choose_btn.text = 'Loaded'
            self.suspect_values = [type_cata,final_model_n,img_name]
            self.suspect_img = img_name
            self.classify_disease()

            # cv2.waitKey(0)
            # self.capture.release()
            # cv2.destroyAllWindows()
        else: Snackbar(text='Select s category then scan an image.' ).open()

    def classify_disease(self):
        suspect_values = self.suspect_values
        threshold = 0.65 # MINIMUM PROBABILITY TO CLASSIFY



        sql = "SELECT Disease_type FROM `disease_info` WHERE `Category` = %s"
        MyCursor.execute(sql,self.suspect_values[0])
        catagory = [x for tupl in MyCursor.fetchall() for x in tupl]

        pickle_in = open(self.suspect_values[1],"rb")
        model = pickle.load(pickle_in)

        imgOriginal = cv2.imread(self.suspect_img)
        img = np.asarray(imgOriginal)
        img = cv2.resize(img,(32,32))
        img = self.preProcessing(img)
        img = img.reshape(1,32,32,1)
        Class_index = int(model.predict_classes(img))
        self.d_class = catagory[Class_index]

        predictions = model.predict(img)
        probVal= np.amax(predictions)

        probVal = Decimal(float(probVal*100))
        probVal = self.round_2(probVal)
        probVal = round(probVal,2)
        ac = '('+str(probVal)+'%)'

        print(Class_index," catagory = ",self.d_class," ac: "+ac)
        self.screen.get_screen('home').ids.disease_name.text = f"> {catagory[Class_index]}"
        self.screen.get_screen('home').ids.probability.text = ac
        # Snackbar(text='Successfully identified suspect image.' ).open()
        self.suspect_values.append(Class_index)
        self.show_selected_img()

    def preProcessing(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        img = img/255
        return img
    def round_2(self, probVal):
        if probVal>=97:
            return float(probVal)-0.47
        else: return probVal

    def show_selected_img(self):
        from kivy.uix.image import Image
        tem_img = ''
        if self.suspect_img!='': 
            tem_img = self.suspect_img
            pop = Popup(title=self.d_class+' image', content=Image(source=tem_img), size_hint=(None, None), size=(345, 380))
            pop.open()
        else:
            pop = Popup(title='Sorry',content=MDLabel(text='No image selected', halign='center',theme_text_color= "Custom", text_color= (1, 1, 1, 1)), size_hint=(None, None), size=(300, 300))
            pop.open()
            # Snackbar(text='Error!!! You havn\'t Chosen any image here.' ).open()
        tem_img=''

    def get_treatment(self):
        self.screen.get_screen('home').ids.treat_symptom.text =''
        if len(self.suspect_values)==4:
            sql = "SELECT Solution FROM `disease_info` WHERE `Category` = %s AND `id` = %s"
            MyCursor.execute(sql,(self.suspect_values[0],self.suspect_values[3]))
            data_099 = MyCursor.fetchone()
            data = data_099[0]
            self.screen.get_screen('home').ids.treat_symptom.text = data
        else: self.screen.get_screen('home').ids.treat_symptom.text = 'No image selected'

    def get_symptom(self):
        self.screen.get_screen('home').ids.treat_symptom.text =''
        if len(self.suspect_values)==4:
            sql = "SELECT Symptom FROM `disease_info` WHERE `Category` = %s AND `id` = %s"
            MyCursor.execute(sql,(self.suspect_values[0],self.suspect_values[3]))
            data_099 = MyCursor.fetchone()
            data = data_099[0]
            self.screen.get_screen('home').ids.treat_symptom.text = data
        else:
            self.screen.get_screen('home').ids.treat_symptom.text = 'No image selected'

    def home_page_clear(self):
        self.suspect_img=''
        self.suspect_values.clear()
        self.screen.get_screen('home').ids.drop_item.text = 'Category'
        # self.screen.get_screen('home').ids.disease_name.text = 'No class disease'
        self.screen.get_screen('home').ids.disease_name.text = '> Clean window'
        self.screen.get_screen('home').ids.probability.text = ''

        self.screen.get_screen('home').ids.treat_symptom.text =''
        self.screen.get_screen('home').ids.suspect_img_choose_btn.text = 'Image'

    #__________________Control panel functions _______________________________________________
    def set_val_disease_table(self):
        self.temp_flag_001 = ''
        self.b_user_info_020 = ''
        self.screen.get_screen('admin_control').ids.disease_info_layout.clear_widgets()
        self.screen.get_screen('admin_control').ids.subadmin_info_layout.clear_widgets()
        self.screen.get_screen('admin_control').ids.user_info_layout.clear_widgets()
        self.temp_flag_001=''

        # for disease information table-------------------
        sql = "SELECT `id`, `Category`,`Disease_type` FROM `disease_info` WHERE 1"
        MyCursor.execute(sql)
        data1 = MyCursor.fetchall()
        self.data_tables1 = MDDataTable(
            pos_hint={'center_x': 0.5,'center_y': 0.6},
            size_hint=(0.8, 0.65),
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(30)),
                ("Category", dp(30)),
                ("Disease", dp(40)),],
            row_data=data1)
        self.data_tables1.bind(on_check_press=self.check_press_001)
        self.screen.get_screen('admin_control').ids.disease_info_layout.add_widget(self.data_tables1)


        # for sub-admins----------------
        sql2 = "SELECT `Name`, `Email` FROM `user_info` WHERE `Status` = 1"
        MyCursor.execute(sql2)
        data2 = list(MyCursor.fetchall())

        self.data_tables2 = MDDataTable(
            pos_hint={'center_x': 0.5,'center_y': 0.6},
            size_hint=(0.8, 0.65),
            use_pagination=True,
            check=True,
            column_data=[
                ("Name", dp(40)),
                ("Email", dp(40))],
            row_data=data2)
        self.data_tables2.bind(on_check_press=self.check_press_002)
        self.screen.get_screen('admin_control').ids.subadmin_info_layout.add_widget(self.data_tables2)
        
        # for basic user -----------------
        sql3 = "SELECT `Name`, `Email` FROM `user_info` WHERE `Status` = 0"
        MyCursor.execute(sql3)
        data3 = list(MyCursor.fetchall())

        self.data_tables3 = MDDataTable(
            pos_hint={'center_x': 0.5,'center_y': 0.6},
            size_hint=(0.8, 0.65),
            use_pagination=True,
            check=True,
            column_data=[
                ("Name", dp(40)),
                ("Email", dp(40))],
            row_data=data3)
        self.data_tables3.bind(on_check_press=self.check_press_003)
        self.screen.get_screen('admin_control').ids.user_info_layout.add_widget(self.data_tables3)
        
    def check_press_001(self, instance_table, current_row):
        if self.temp_flag_001=='':
            self.temp_flag_001 = current_row
        elif self.temp_flag_001==current_row:
            self.temp_flag_001=''
        else:
            self.temp_flag_001 = current_row
        # if self.temp_flag_001:
        #     print(self.temp_flag_001)

    def check_press_002(self, instance_table, current_row):
        
        if self.b_subadmin_info_020 =='':
            self.b_subadmin_info_020  = current_row
        elif self.b_subadmin_info_020 ==current_row:
            self.b_subadmin_info_020 =''
        else:
            self.b_subadmin_info_020  = current_row

    def check_press_003(self, instance_table, current_row):
        if self.b_user_info_020=='':
            self.b_user_info_020 = current_row
        elif self.b_user_info_020==current_row:
            self.b_user_info_020=''
        else:
            self.b_user_info_020 = current_row

    def go_to_messenger_from_admin(self):
        if self.b_user_info_020!='':
            mail = self.b_user_info_020[1]
            y_name = self.b_user_info_020[0]
            sql = "UPDATE `message` SET `status` = 1 WHERE `message`.`Email` = %s and `Sender`=%s"
            MyCursor.execute(sql,(mail,y_name))
            conn.commit()

            self.night_monkey_data = [mail,y_name]
            self.single_msg_display()
            MDApp.get_running_app().root.current = "user_message"
            MDApp.get_running_app().root.transition.direction = 'left'
        else:
            Snackbar(text='Please select one row').open()
    def go_to_profile_from_admin(self):
        if self.b_user_info_020!='':
            mail = self.b_user_info_020[1]
            self.night_monkey_data = [mail,'d']
            self.view_profile()
        else:
            Snackbar(text='Please select one row').open()

    def go_to_show_dis(self):
        if self.temp_flag_001:
            sql = "SELECT * FROM `disease_info` WHERE `Category` = %s AND `id` = %s"
            MyCursor.execute(sql,(self.temp_flag_001[1],self.temp_flag_001[0]))
            self.disease_info = MyCursor.fetchone()

            self.screen.get_screen('Add_show_diease').ids.d_category.text=self.disease_info[0]
            self.screen.get_screen('Add_show_diease').ids.d_id.text=str(self.disease_info[1])
            self.screen.get_screen('Add_show_diease').ids.d_disease_name.text=self.disease_info[2]
            self.screen.get_screen('Add_show_diease').ids.d_treatment.text=self.disease_info[3]
            self.screen.get_screen('Add_show_diease').ids.d_more.text=self.disease_info[4]

            MDApp.get_running_app().root.current = "Add_show_diease"
            MDApp.get_running_app().root.transition.direction = 'left'
        else:
            Snackbar(text='Please select one item').open()
            
    def go_to_add_new_dis(self):
        self.screen.get_screen('Add_show_diease').ids.d_category.text=''
        self.screen.get_screen('Add_show_diease').ids.d_id.text=''
        self.screen.get_screen('Add_show_diease').ids.d_disease_name.text=''
        self.screen.get_screen('Add_show_diease').ids.d_treatment.text=''
        self.screen.get_screen('Add_show_diease').ids.d_more.text=''

        MDApp.get_running_app().root.current = "Add_show_diease"
        MDApp.get_running_app().root.transition.direction = 'left'      


    def add_disease_to_database(self):
        add_d_0 = self.screen.get_screen('Add_show_diease').ids.d_category.text
        add_d_1 = self.screen.get_screen('Add_show_diease').ids.d_id.text
        add_d_2 = self.screen.get_screen('Add_show_diease').ids.d_disease_name.text
        add_d_3 = self.screen.get_screen('Add_show_diease').ids.d_treatment.text
        add_d_4 = self.screen.get_screen('Add_show_diease').ids.d_more.text

        self.admin_close_insert_flag=0
        closebtn = MDFlatButton(text='OK', on_release=self.close_dialog5)
        
        if add_d_0!='' and add_d_1!=''and add_d_2!='' and add_d_3!='' and add_d_4!='':
            try:
                sql = "INSERT INTO `disease_info` VALUES (%s, %s, %s, %s, %s)"
                MyCursor.execute(sql,(add_d_0,add_d_1,add_d_2,add_d_3,add_d_4))
                conn.commit()
                self.set_val_disease_table()
                self.dialog5 = MDDialog(title="Insert successfull",text='Data inserted successfully', size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog5.open()
            except:
                self.dialog5 = MDDialog(title="Error",text='Something went worng\nTry again', size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog5.open()
                self.admin_close_insert_flag=1
                
        else:
            Snackbar(text='Please fill up all the fields').open()
    def close_dialog5(self,args):
        self.dialog5.dismiss()
        if self.admin_close_insert_flag==0:
            MDApp.get_running_app().root.current = "admin_control"
            MDApp.get_running_app().root.transition.direction = 'right'  
        

    def update_disease_to_database(self):
        add_d_0 = self.screen.get_screen('Add_show_diease').ids.d_category.text
        add_d_1 = self.screen.get_screen('Add_show_diease').ids.d_id.text
        add_d_2 = self.screen.get_screen('Add_show_diease').ids.d_disease_name.text
        add_d_3 = self.screen.get_screen('Add_show_diease').ids.d_treatment.text
        add_d_4 = self.screen.get_screen('Add_show_diease').ids.d_more.text

        add_d_5 = self.temp_flag_001[1]
        add_d_6 = int(self.temp_flag_001[0])

        closebtn = MDFlatButton(text='OK', on_release=self.close_dialog6)

        if add_d_0!='' and add_d_1!=''and add_d_2!='' and add_d_3!='' and add_d_4!='':
            try:
                sql = "UPDATE `disease_info` SET `Category`= %s, `id`=%s, `Disease_type`=%s, `Solution`=%s, `Symptom`=%s WHERE `disease_info`.`Category` = %s AND `disease_info`.`id` = %s"
                MyCursor.execute(sql,(add_d_0,add_d_1,add_d_2,add_d_3,add_d_4,add_d_5, add_d_6))
                conn.commit()
                self.set_val_disease_table()
                self.dialog6 = MDDialog(title="Update successfull",text='Data updated successfully', size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog6.open()
            except Exception as e:
                self.dialog6 = MDDialog(title="Error",text='Something went worng\nTry again', size_hint=(0.8,0.5), buttons=[closebtn])
                self.dialog6.open()
                print(e)
                
        else:
            Snackbar(text='Please fill up all the fields').open()
    def close_dialog6(self,args):
        self.dialog6.dismiss()

    def disease_info_del(self):
        closebtn1 = MDFlatButton(text='Yes', on_release=self.close_dialog7_1)
        closebtn2 = MDFlatButton(text='No', on_release=self.close_dialog7_2)
        if self.temp_flag_001:
            self.dialog7 = MDDialog(title="Conformation",text='Are you sure to delete the data', size_hint=(0.8,0.5), buttons=[closebtn2,closebtn1])
            self.dialog7.open()
        else:
             Snackbar(text='Please select one row').open()

    def close_dialog7_1(self,args):
        del_info_0 = self.temp_flag_001[1]
        del_info_1 = self.temp_flag_001[0]
        sql = "DELETE FROM `disease_info` WHERE `disease_info`.`Category` = %s AND `disease_info`.`id` = %s"
        MyCursor.execute(sql,(del_info_0, del_info_1))
        conn.commit() 
        self.set_val_disease_table()
        self.dialog7.dismiss()

    def close_dialog7_2(self,args):
        self.dialog7.dismiss()

    def make_user_to_admin(self):
        closebtn1 = MDFlatButton(text='Yes', on_release=self.close_dialog8_1)
        closebtn2 = MDFlatButton(text='No', on_release=self.close_dialog8_2)
        if self.b_user_info_020 != '':
            self.dialog8 = MDDialog(title="Conformation",text='Are you sure to set the user as sub-admin?', size_hint=(0.8,0.5), buttons=[closebtn2,closebtn1])
            self.dialog8.open()
        else:
            Snackbar(text='Please select one row').open()

    def close_dialog8_1(self,args):
        sql = "UPDATE `user_info` SET `Status` = 1 WHERE `user_info`.`Email` = %s"
        MyCursor.execute(sql,self.b_user_info_020[1])
        conn.commit()
        self.set_val_disease_table()
        self.dialog8.dismiss()

    def close_dialog8_2(self,args):
        self.dialog8.dismiss()

    def remove_subadmin_98(self):
        closebtn1 = MDFlatButton(text='Yes', on_release=self.close_dialog9_1)
        closebtn2 = MDFlatButton(text='No', on_release=self.close_dialog9_2)
        if self.b_subadmin_info_020 != '':
            self.dialog9 = MDDialog(title="Conformation",text='Are you sure to remove from sub-admin?', size_hint=(0.8,0.5), buttons=[closebtn2,closebtn1])
            self.dialog9.open()
        else:
            Snackbar(text='Please select one row').open()

    def close_dialog9_1(self,args):
        sql = "UPDATE `user_info` SET `Status` = 0 WHERE `user_info`.`Email` = %s"
        MyCursor.execute(sql,self.b_subadmin_info_020[1])
        conn.commit()
        self.set_val_disease_table()
        self.dialog9.dismiss()

    def close_dialog9_2(self,args):
        self.dialog9.dismiss()
        
    def go_to_profile_from_admin2(self):
        if self.b_subadmin_info_020!='':
            mail = self.b_subadmin_info_020[1]
            self.night_monkey_data = [mail,'d']
            self.view_profile()
        else:
            Snackbar(text='Please select one row').open()

    #__________________ Messaging functions ___________________________________________________

    def  goto_message_control(self):
        if self.user_login_data[5]==2:
            self.admin_message_show()
            self.set_val_disease_table()
            MDApp.get_running_app().root.current = "admin_control"
            MDApp.get_running_app().root.transition.direction = 'left'
        else:
            sql = "UPDATE `message` SET `status` = '1' WHERE `Email` = %s and `Sender`=%s"
            MyCursor.execute(sql,(self.user_login_data[1],'Admin'))
            conn.commit()
            self.show_msg()
            MDApp.get_running_app().root.current = "user_message"
            MDApp.get_running_app().root.transition.direction = 'left'

    def show_msg(self):
        values = self.user_login_data
        sql = "SELECT * FROM `message` WHERE `Email` = %s"
        MyCursor.execute(sql,values[1])
        data = MyCursor.fetchall()

        if len(data)>15:
            l = len(data) - 15
            sql = "SELECT * FROM `message` WHERE `Email` = %s LIMIT 15 OFFSET %s"
            MyCursor.execute(sql,(values[1],l))
            data = MyCursor.fetchall()
        else:
            pass
        conn.commit()

        self.screen.get_screen('user_message').ids.container.clear_widgets()
        for rec in data: 
            if rec[1]=='Admin':
                path_004 = 'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/icons/icon_img.png'
                img_ava = ImageLeftWidget(source=path_004)

            else:
                imgr_name = values[1].split('@')[0]
                path_004 = f'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{imgr_name}.jpg'
                img_ava = ImageLeftWidget(source=path_004)

            items = TwoLineAvatarIconListItem(text=rec[1], secondary_text=f"[size=13]{rec[2]}")
            items.add_widget(img_ava)
            self.screen.get_screen('user_message').ids.container.add_widget(items)
        # threading.Timer(3, self.show_msg).start()

    def send_msg(self):
        values = self.user_login_data
        messagen = self.screen.get_screen('user_message').ids.message_new.text
        if messagen!='':
            date_time = self.get_cur_time()
            sql = "INSERT INTO `message`(`Email`, `Sender`, `Message`, `status`, `date_time`, `id`) VALUES (%s, %s, %s, '0', %s, NULL)"
            MyCursor.execute(sql,(values[1],values[0],messagen,date_time))
            conn.commit()
            self.show_msg()
        self.screen.get_screen('user_message').ids.message_new.text = ''

    # message system for admin --------------------------------
    def admin_message_show(self):
        self.ck_delete_list.clear()
        self.screen.get_screen('admin_control').ids.message_list.clear_widgets()
        sql = "SELECT DISTINCT Email FROM message GROUP BY Email ORDER BY MAX(date_time) DESC, Email"
        MyCursor.execute(sql)
        data = MyCursor.fetchall()
        data = [x for tupl in data for x in tupl]
        conn.commit()
        self.screen.get_screen('admin_control').ids.message_list.clear_widgets()
        for rec in data:
            sender_info = self.get_sender_info(rec)
            
            items = TwoLineAvatarIconListItem(text=sender_info[1], secondary_text=f"[size=13]{sender_info[3]}    {sender_info[2]}",on_release=partial(self.show_individual_msg,rec))
            items.add_widget(ImageLeftWidget(source=sender_info[0]))
            right_I = IconRightWidget(icon='icons/nothing.png')
            
            ck = MDCheckbox(active= False)
            ck.bind(on_release=partial(self.check_press_f,rec))
            right_I.add_widget(ck)
            items.add_widget(right_I) 
            self.screen.get_screen('admin_control').ids.message_list.add_widget(items)
            
    def check_press_f(self,val, xxyy):
        self.ck_delete_list.append(val)

    def delete_msg_call(self):
        list_user_msg = set(self.ck_delete_list)
        list_user_msg = list(list_user_msg)
        print(list_user_msg)

    def get_sender_info(self,rec):
        sql = "SELECT * FROM `message` WHERE `Email`=%s ORDER BY date_time DESC"
        MyCursor.execute(sql,rec)
        data = MyCursor.fetchall()
        conn.commit()
        img_name = rec.split('@')[0]
        img_path = f'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{img_name}.jpg'
        new_time = self.formated_date(data[0][4])

        sql1 = "SELECT Name FROM `user_info` WHERE `Email`=%s"
        MyCursor.execute(sql1,rec)
        name = MyCursor.fetchall()
        name = name[0][0]

        sql2 = "SELECT COUNT(*) FROM message WHERE `Email` = %s and `Sender`=%s and status=0"
        MyCursor.execute(sql2,(rec,name))
        data2 = MyCursor.fetchall()
        num_of_unread_message = [x for tupl in data2 for x in tupl]

        sql3 = "SELECT * FROM `message` WHERE `Email`=%s ORDER BY date_time DESC"
        MyCursor.execute(sql3,rec)
        fg_check = MyCursor.fetchall()
        # print(fg_check[0][1])

        flag = '( Seen )'
        if num_of_unread_message[0]!=0:
            flag=f' ({num_of_unread_message[0]} new)'
        elif fg_check[0][1]=='Admin':
            flag='(Replied)'

        lst = [img_path,name,new_time,flag]
        return lst

    def show_individual_msg(self,mail,y):
        sql = "UPDATE `message` SET `status` = 1 WHERE `message`.`Email` = %s and `Sender`=%s"
        MyCursor.execute(sql,(mail,y.text))
        conn.commit()

        self.night_monkey_data = [mail,y.text]
        self.single_msg_display()
        MDApp.get_running_app().root.current = "user_message"
        MDApp.get_running_app().root.transition.direction = 'left'

    def single_msg_display(self):
        self.screen.get_screen('user_message').ids.container.clear_widgets()
        sql = "SELECT * FROM `message` WHERE `Email` = %s"
        MyCursor.execute(sql,self.night_monkey_data[0])
        data = MyCursor.fetchall()

        if len(data)>15:
            l = len(data) - 15
            sql = "SELECT * FROM `message` WHERE `Email` = %s LIMIT 15 OFFSET %s"
            MyCursor.execute(sql,(values[1],l))
            data = MyCursor.fetchall()
        else: pass
        conn.commit()
        
        for rec in data:
            alig = 'left'
            if rec[1]=='Admin':
                path_004 = 'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/icons/icon_img.png'
                img_ava = ImageLeftWidget(source=path_004)
                alig='right'
            else:
                imgr_name = self.night_monkey_data[0].split('@')[0]
                path_004 = f'D:/Working_dir/Programming/Python/Mini_Agriculturist-2/User_images/{imgr_name}.jpg'
                img_ava = ImageLeftWidget(source=path_004)

            items = TwoLineAvatarIconListItem(text=rec[1], secondary_text=f"[size=13]{rec[2]}")
            items.halign = 'right'
            items.add_widget(img_ava)
            self.screen.get_screen('user_message').ids.container.add_widget(items)
        self.screen.get_screen('user_message').ids.messager_to.title=self.night_monkey_data[1]

    def send_msg_admin(self):
        messagen = self.screen.get_screen('user_message').ids.message_new.text
        values = self.night_monkey_data
        if messagen!='':
            date_time = self.get_cur_time()
            sql = "INSERT INTO `message`(`Email`, `Sender`, `Message`, `status`,`date_time`, `id`) VALUES (%s, %s, %s, '0',%s, NULL)"
            MyCursor.execute(sql,(values[0],'Admin',messagen,date_time))
            conn.commit()
            self.single_msg_display()
        self.screen.get_screen('user_message').ids.message_new.text = ''

    def back_from_messenger(self):
        if self.user_login_data[5]==2:
            self.admin_message_show()
            MDApp.get_running_app().root.current = "admin_control"
            MDApp.get_running_app().root.transition.direction = 'right'
        else: self.go_to_home()

    def refresh_messages(self):
        if self.user_login_data[5]==2: 
            self.single_msg_display()
        else: self.show_msg()

    def send_msg__all(self):
        if self.user_login_data[5]==2: self.send_msg_admin()
        else: self.send_msg()

    def get_cur_time(self):
        x = datetime.datetime.now()

        date = f"{x.strftime('%y')}-{x.strftime('%m')}-{x.strftime('%d-')}"
        time = f"{x.strftime('%H')}-{x.strftime('%M')}"
        dT = date+time
        return dT
    def formated_date(self,date_time):
        month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        a_p = 'AM'
        dtime = date_time.split('-')
        if int(dtime[3])>12:
            dtime[3] = int(dtime[3])-12
            a_p = 'PM'
        
        new_time = f"[{dtime[3]}:{dtime[4]} {a_p},  {dtime[2]}-{dtime[1]}-{dtime[0]}]"
        return new_time

    def check_connection(self):
        host='http://google.com'
        try:
            urec.urlopen(host)
            return True
        except: return False

if __name__=='__main__':
    DemoApp().run()
