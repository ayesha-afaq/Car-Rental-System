import os
import pyodbc
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

import pandas as pd
from abc import ABC,abstractmethod

ADMIN_PASSWORD_FILE='adminpass.txt'
Connection_String='connection.txt'
class User:
   def __init__(self):
      self.name=None
      self.password=None
      self.balance=None
      #idr user qindow bnegi jismai login , create user ka option hoga , if user clicks on create user then create user ka window khulega wrna login ka
      self.CreateUserWindow()


   def ShowOperations(self):

      pass
   def CreateUser(self,name,password,balance):
      self.name=name
      self.password=password
      self.balance=balance
      
      self.db=RecordManagement("Users")
      self.db.insert(self.name,self.password,self.balance)

   def CreateUserWindow(self):
      create_user_window=ctk.CTk()
      self.create_user_window=create_user_window
      self.admin_window.title('Create User')
      self.admin_window.geometry('450x450')
      self.create_user_Frame=CTkFrame(create_user_window, width=500, height=500)
      self.create_user_Frame.pack(pady=40)
      # CTkButton(master=self.admin_frame,text='ADD CAR',corner_radius=10,fg_color='blue').pack(pady=10)
      
      name=CTkEntry(self.create_user_Frame,placeholder_text='Enter your name')
      name.place(relx=0.5,rely=0.4,anchor='center')
      password=CTkEntry(self.create_user_Frame,placeholder_text='Enter your password')
      password.place(relx=0.5,rely=0.4,anchor='center')
      balance=CTkEntry(self.create_user_Frame,placeholder_text='Enter your balance')
      balance.place(relx=0.5,rely=0.4,anchor='center')
      CTkButton(master=self.create_user_Frame,text='Create User',command=lambda: self.CreateUser(name.get(),password.get(),balance.get()),corner_radius=10,fg_color='blue').pack(pady=10)
      create_user_window.mainloop()

class RecordManagement:
   def __init__(self,TableName):
      self.TableName=TableName
      try:
         with open(Connection_String) as cs_file:
            self.cs=cs_file.read().strip()
         self.connection=pyodbc.connect(self.cs)
         print('connected to database')
         
         

      except Exception as e:
         print('connection error')
         messagebox('Connection Error',e,error=True)
         return
      else:
         self.connection.autocommit=True
         self.cursor=self.connection.cursor()

   def insert(self,*args):
      
      if self.TableName=='Users':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (NAME, PASSWORD, BALANCE) VALUES (?, ?, ?)",
                           (args[0], args[1], args[2])  
)

      
         
     
      

   
      

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

class Car:
   pass

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
      self.admin_frame =CTkFrame(admin_window, width=500, height=500)
      self.admin_frame.pack(pady=40)
      CTkButton(master=self.admin_frame,text='ADD CAR',corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='REMOVE CAR',corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='CURRENTLY RESERVED CARS',corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='CURRENT RENTALS REPORT',corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='CHANGE PASSWORD',command=self.ChangePassword,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='BACK TO HOME PAGE',command=self.back_home,corner_radius=10,fg_color='blue').pack(pady=10)

      admin_window.mainloop()

   def back_home(self):
      try:
         self.admin_window.destroy()
         print('admin window destroyed')
      except:
         print('unknown error')

   def ChangePassword(self):
      try:
         new_pass=CTkInputDialog(text='Enter New Password',title='Change Password').get_input()
         with open(ADMIN_PASSWORD_FILE,'w') as f:
            f.write(new_pass)
            messagebox('Change Password','Password Changed Successfully :)')
      except:
         messagebox('Unknown Error','Please Enter Valid Password',error=True)
      
   def add_car(self):
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
      CTkButton(master=self.menu_frame,text='USER ACCOUNT',command=lambda: User(),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='ADMINISTRATOR',command=self.admin_work,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='EXIT SYSTEM',command=self.destroy_window,corner_radius=10,fg_color='blue').pack(pady=10)

   def destroy_window(self):

      #exits the system
      self.root.quit()    
      self.root.destroy()
       
   def admin_work(self):
      if os.path.isfile(ADMIN_PASSWORD_FILE): ## checks if given path ki file exist krti hae 
         print('file exists')
         with open(ADMIN_PASSWORD_FILE) as pass_file:
            p=pass_file.read().strip()
         password=CTkInputDialog(text='Enter Password',title='Admin Login').get_input()
         
         if p==password:
            print('good')
            # messagebox('Success','Access Granted To Admin Account')
            # Hide the main window
            # self.root.withdraw()
            self.admin=Admin(password)
            
            # Show the main window again
            
            # self.root.deiconify()
            # print('hello')
            
         else: 
            print('not gud')
            messagebox('Access Blocked','Incorrect Password',error=True)

         # Show the main window again
         # self.root.deiconify()
      



root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
