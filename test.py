import os
import pyodbc
# import customtkinter as ctk
# from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel

# ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('green')
# root=ctk.CTk()
Connection_String='ConnectionStringayesha.txt'

try:
   with open(Connection_String) as cs_file:
      cs=cs_file.read().strip()
      print(cs)
      connection=pyodbc.connect(cs)
      print('connected to database')
except Exception as e:
         print('connection error')
         # messagebox('Connection Error',e,error=True)
         # return

# root.mainloop()

