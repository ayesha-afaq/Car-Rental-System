import os
import pyodbc
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')
root=ctk.CTk()

def func():
   root.withdraw()
   print('hello')
   print('hello')
   print('hello')
   print('window coming back')
   
   root.deiconify()
   print('window came')

CTkButton(root,text='window1\npress',command=func).pack()




# def func():
#     print(entry.get())
#     print(entry)

# root=ctk.CTk()
# entry=CTkEntry(root,placeholder_text='Enter your name')
# entry.place(relx=0.5,rely=0.4,anchor='center')
# entrybutton=CTkButton(root,text='Submit',command=func)
# entrybutton.place(relx=0.5,rely=0.5,anchor='center')


root.mainloop()

