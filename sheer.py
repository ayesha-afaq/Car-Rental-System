import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

import pandas as pd
from abc import ABC,abstractmethod


class Account(ABC):
   def __init__(self,username,password,check):
      self.username=username
      self.password=password
      self.check=check
   def ChangePassword(self,newPass):
      self.password=newPass

   @abstractmethod
   def ShowOperations(self):
      pass

class User(Account):
   def __init__(self,user_name,pass_word):
      Account.__init__(self,user_name,pass_word)


class Admin(Account):
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
      CTkButton(master=self.menu_frame,text='ADMINISTRATOR',corner_radius=10,fg_color='blue').pack(pady=10)
      



root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
