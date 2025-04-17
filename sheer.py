import os
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

import pandas as pd
from abc import ABC,abstractmethod

ADMIN_PASSWORD_FILE='adminpass.txt'

def messagebox(title, message,error=False):
    ## custom tkinter mAE message box khud sae nhi arha tha tu is liyay yay bnya hAE
    top = CTkToplevel()
    top.title(title)
    top.geometry("300x200")
    top.resizable(False, False)
    if error==True:
        CTkLabel(top,text="⚠️",font=("Arial", 24)).pack(pady=10)
    # Message
    CTkLabel(top, text=message).pack(pady=30)
    
    # OK button (closes the window)
    CTkButton(top, text="OK", command=top.destroy).pack()


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
      self.ShowOperations()

   def ShowOperations(self):
      admin_window=ctk.CTk()
      self.admin_window=admin_window
      self.admin_window.title('Admin')
      self.admin_window.geometry('450x450')

      admin_window.mainloop()

class Rental_System:
   
   def __init__(self,root):
      self.root=root
      self.root.title('CAR RENTAL SYSTEM')
      self.root.geometry('500x500')
      header=CTkLabel(
         self.root,
         width=10,
         corner_radius=10,
         text='Welcome To The Car Rental System\n',
         font=("Times New Roman", 20)).pack(pady=20)
      header2=CTkLabel(
         self.root,
         width=10,
         corner_radius=10,
         text='\nPlease Choose Your Account Type',
         font=("Arial", 16)).pack(pady=10)
         
      self.menu_frame =CTkFrame(root, width=500, height=500)
      self.menu_frame.pack(pady=40)
      CTkButton(master=self.menu_frame,text='USER ACCOUNT',corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='ADMINISTRATOR',command=self.admin_work,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='EXIT SYSTEM',command=self.destroy_window,corner_radius=10,fg_color='blue').pack(pady=10)

   def destroy_window(self):

      #exits the system
      self.root.quit()    
      self.root.destroy()
       
   def admin_work(self):
      if not os.path.isfile(ADMIN_PASSWORD_FILE): ## checks if given path ki file exist krti hae
         with open(ADMIN_PASSWORD_FILE,'w') as f:
            password=CTkInputDialog(text='Set Password',title='Creating Admin Account').get_input()
            f.write(password)
                  
         self.admin=Admin(password)
         self.admin.ShowOperations()
         print('admin made ')
      else: 
         print('file exists')
         with open(ADMIN_PASSWORD_FILE) as pass_file:
            p=pass_file.read().strip()
         password=CTkInputDialog(text='Enter Password',title='Admin Login').get_input()
         
         if p==password:
            print('good')
            messagebox('Success','Access Granted To Admin Account')
            self.admin.ShowOperations() ##ispe error arha hai idk whyyyyyyy
            # Hide the main window
            # self.root.withdraw()
               
         else: 
            print('not gud')
            messagebox('Access Blocked','Incorrect Password')



         # Show the main window again
         # self.root.deiconify()
      



root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
