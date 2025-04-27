import os
import pyodbc
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel


import pandas as pd
from abc import ABC,abstractmethod

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')


ADMIN_PASSWORD_FILE='adminpass.txt'
Connection_String=r"C:\Users\maham\OneDrive\Desktop\gitdemo\project\ConnectionStringmaham.txt" ## apne pass krna hu tu apna naam daldena


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
                           f"INSERT INTO {self.TableName} (USER_NAME,NAME, PASSWORD, BALANCE,ADDRESS) VALUES (?, ?, ?, ?, ?)",
                           (args[0], args[1], args[2],args[3],args[4]))
     
      elif self.TableName=='Cars':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (BRAND, MODEL, PricePerDay, SeatingCapacity) VALUES (?, ?, ?, ?)",
                           (args[0], args[1], args[2],args[3]))
      elif self.TableName=='RentalHistory':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (USER_ID, CAR_ID, START_DATE, END_DATE) VALUES (?, ?, ?, ?)",
                           (args[0], args[1], args[2],args[3]))
         
      elif self.TableName=='Admin':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (USER_NAME, PASSWORD) VALUES (?, ?)",
                           (args[0], args[1]))
         
   def fetch(self,operation,*args):
      if self.TableName=='Users':
         if operation=="login":
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE USER_NAME='{args[0]}' AND PASSWORD='{args[1]}'")
            return self.cursor.fetchall()


class Account(ABC):
      
   def ChangePassword(self,account):
      change_pass_window=ctk.CTk()
      self.change_pass_window=change_pass_window
      self.change_pass_window.title('Change Password')
      self.pass_Frame=CTkFrame(self.change_pass_window,width=500, height=500)
      
      password=CTkEntry(master=self.pass_Frame,placeholder_text='Enter your new password',corner_radius=10,fg_color='blue')
      password.pack(pady=10)
      CTkButton(master=self.pass_Frame,text='Enter',command=lambda: Change(password.get())).pack(pady=20)


      def Change(password):
         if account=='Admin':
            ####2 query: changes the password in admin table
            pass
         elif account=='User':
            #2 query: changes passowrd in user table
            pass


   @abstractmethod
   def ShowOperations(self):
      pass
   
   
class User(Account):
   def __init__(self):
      self.name=None
      self.password=None
      self.balance=None
      self.address=None
      user_window=ctk.CTk()
      self.user_window=user_window
      self.user_window.title('User Portal')
      self.user_window.geometry('450x450')
      self.user_Frame=CTkFrame(user_window, width=500, height=500)
      self.user_Frame.pack(pady=40)
      CTkButton(master=self.user_Frame,text='Sign in',command=lambda: self.CreateUserWindow(),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_Frame,text='Log in',command=lambda: self.LoginWindow(),corner_radius=10,fg_color='blue').pack(pady=10)
      user_window.mainloop()
      #idr user qindow bnegi jismai login , create user ka option hoga , if user clicks on create user then create user ka window khulega wrna login ka
   

   def LoginWindow(self):
      login_window=ctk.CTk()
      self.login_window=login_window
      self.login_window.title('Login')
      self.login_window.geometry('450x450')
      self.login_Frame=CTkFrame(login_window, width=500, height=500)
      self.login_Frame.pack(pady=40)
      # CTkButton(master=self.admin_frame,text='ADD CAR',corner_radius=10,fg_color='blue').pack(pady=10)
      
      user_name=CTkEntry(master=self.login_Frame,placeholder_text='Enter your username',corner_radius=10,fg_color='blue')
      user_name.pack(pady=10)
      
      password=CTkEntry(master=self.login_Frame,placeholder_text='Enter your password',corner_radius=10,fg_color='blue')
      password.pack(pady=10)
      CTkButton(master=self.login_Frame,text='Log in',command=lambda: self.Login(user_name.get(),password.get()),corner_radius=10,fg_color='blue').pack(pady=10)
      login_window.mainloop()

   def Login(self,username,password):
      # self.username=username
      # self.password=password
      self.db=RecordManagement("Users")
      result=self.db.fetch('login',username,password)
      if len(result)==0:
         messagebox('Login Failed','Invalid Username or Password',error=True)
         return
      else:
         messagebox('Login Success','Welcome to the Car Rental System :)')
         print('login success')
         self.ShowOperations()
      
   def ShowOperations(self):
      ## inme change password ka option bhi rkhna hae jo admin aur user kai liyay same hoga account class sae inherit hoga
      pass
   def CreateUser(self,name,username,password,balance,address):
      self.username=username
      self.name=name
      self.password=password
      self.balance=balance
      self.address=address
      
      self.db=RecordManagement("Users")
      self.db.insert(self.username,self.name,self.password,self.balance,self.address)

   def CreateUserWindow(self):
      create_user_window=ctk.CTk()
      self.create_user_window=create_user_window
      self.create_user_window.title('Create User')
      self.create_user_window.geometry('450x450')
      self.create_user_Frame=CTkFrame(create_user_window, width=500, height=500)
      self.create_user_Frame.pack(pady=40)
      # CTkButton(master=self.admin_frame,text='ADD CAR',corner_radius=10,fg_color='blue').pack(pady=10)
      
      name=CTkEntry(master=self.create_user_Frame,placeholder_text='Enter your name',corner_radius=10,fg_color='blue')
      name.pack(pady=10)
      user_name=CTkEntry(master=self.create_user_Frame,placeholder_text='Enter your username',corner_radius=10,fg_color='blue')
      user_name.pack(pady=10)
      
      password=CTkEntry(master=self.create_user_Frame,placeholder_text='Enter your password',corner_radius=10,fg_color='blue')
      password.pack(pady=10)
      balance=CTkEntry(master=self.create_user_Frame,placeholder_text='Enter your balance',corner_radius=10,fg_color='blue')
      balance.pack(pady=10)
      address=CTkEntry(master=self.create_user_Frame,placeholder_text='Enter your address',corner_radius=10,fg_color='blue')
      address.pack(pady=10)
      CTkButton(master=self.create_user_Frame,text='Create User',command=lambda: self.CreateUser(name.get(),user_name.get(),password.get(),balance.get(),address.get()),corner_radius=10,fg_color='blue').pack(pady=10)
      create_user_window.mainloop()




class Admin(Account):
   def __init__(self):
      admin_login_window=ctk.CTk()
      self.admin_login_window=admin_login_window
      self.admin_login_window.title('Login Admin Account')
      self.admin_login_window.geometry('450x450')
      self.admin_login_Frame=CTkFrame(admin_login_window, width=500, height=500)
      self.admin_login_Frame.pack(pady=40)
      
      user_name=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Username',corner_radius=10,fg_color='green')
      user_name.pack(pady=10)
      
      password=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Password',corner_radius=10,fg_color='green')
      password.pack(pady=10)
      
      CTkButton(master=self.admin_login_Frame,text='Login',command=lambda: self.ShowOperations(user_name.get(),password.get()),corner_radius=10,fg_color='blue').pack(pady=20)
      admin_login_window.mainloop()


   def ShowOperations(self,username,password):


      ## 1. query for checks kae username aur password sahi hain ya nhi

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
      CTkButton(master=self.admin_frame,text='CHANGE PASSWORD',command= lambda: self.ChangePassword(account='Admin'),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.admin_frame,text='BACK TO HOME PAGE',command=self.back_home,corner_radius=10,fg_color='blue').pack(pady=10)

      admin_window.mainloop()

   def back_home(self):
      try:
         self.admin_window.destroy()
         print('admin window destroyed')
      except:
         print('unknown error')

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
      CTkButton(master=self.menu_frame,text='ADMINISTRATOR',command=lambda: Admin(),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='EXIT SYSTEM',command=self.destroy_window,corner_radius=10,fg_color='blue').pack(pady=10)

   def destroy_window(self):

      #exits the system
      self.root.quit()    
      self.root.destroy()
       
   # def admin_work(self):
   #    if os.path.isfile(ADMIN_PASSWORD_FILE): ## checks if given path ki file exist krti hae 
   #       print('file exists')
   #       with open(ADMIN_PASSWORD_FILE) as pass_file:
   #          p=pass_file.read().strip()
   #       password=CTkInputDialog(text='Enter Password',title='Admin Login').get_input()
         
   #       if p==password:
   #          print('good')
   #          # messagebox('Success','Access Granted To Admin Account')
   #          # Hide the main window
   #          # self.root.withdraw()
   #          self.admin=Admin(password)
            
   #          # Show the main window again
            
   #          # self.root.deiconify()
   #          # print('hello')
            
   #       else: 
   #          print('not gud')
   #          messagebox('Access Blocked','Incorrect Password',error=True)

   #       # Show the main window again
   #       # self.root.deiconify()
      



root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
