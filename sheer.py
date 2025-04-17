import os
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

import pandas as pd
from abc import ABC,abstractmethod

ADMIN_PASSWORD_FILE='adminpass.txt'

class Account(ABC):
   def __init__(self,password):
      # self.username=username
      self.password=password
      
   def ChangePassword(self,newPass):
      self.password=newPass

   @abstractmethod
   def ShowOperations(self):
      pass

class User(Account):
   def __init__(self,user_name,pass_word):
      Account.__init__(self,pass_word)
      self.username=user_name


class Admin(Account):
   def __init__(self, password):
      super().__init__(password)
      
   def ShowOperations(self):
      pass

class Rental_System:
   
   def __init__(self,root):
         self.root=root
         self.root.title('CAR RENTAL SYSTEM')
         self.root.geometry('500x500')
         header=CTkLabel(
            self.root,
            width=10,
            corner_radius=10,
            text='Welcome To The Car Rental System\n\nPlease Choose Your Account Type',
            font=("Arial", 16)).pack(pady=20)

         
         
         self.menu_frame =CTkFrame(root, width=500, height=500)
         self.menu_frame.pack(pady=40)
         CTkButton(master=self.menu_frame,text='USER ACCOUNT',corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.menu_frame,text='ADMINISTRATOR',command=self.admin_work,corner_radius=10,fg_color='blue').pack(pady=10)

   def admin_work(self):
         if not os.path.isfile(ADMIN_PASSWORD_FILE): ## checks if given path ki file exist krti hae
            with open(ADMIN_PASSWORD_FILE,'w') as f:
                  password=CTkInputDialog(text='Set Password',title='Creating Admin Account').get_input()
                  f.write(password)
                  
            self.admin=Admin(password)
            print('admin made ')
         else: 
            print('file exists')
            with open(ADMIN_PASSWORD_FILE) as pass_file:
               p=pass_file.read().strip()
            
            password=CTkInputDialog(text='Enter Password',title='Admin Login').get_input()
         
            if p==password:
               print('good')
            else: print('not gud')
      



root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
