import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import Label,Button,Frame,Radiobutton



class Rental_System:
   def __init__(self,root):
      self.root=root
      self.root.title("CEP")
      root.geometry("500x500+50+50")
      root.minsize(200, 100)
      root.maxsize(800, 800)
      
      header = Label(self.root,text="|||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CAR RENTAL SYSTEM~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|||")
      header.pack()#Displays a header.
      
      self.menu_frame = tk.Frame(root)
      self.menu_frame.pack(pady=50)
      tk.Button(self.menu_frame, text="USER", width=30,height=5,bg='aqua').pack(pady=30)
      tk.Button(self.menu_frame, text="ADMINISTRATOR", width=30,height=5,bg='aqua').pack(pady=30)





if __name__ == "__main__":
    root=tk.Tk()#Creates the main tkinter window (root).
    app=Rental_System(root)#Initializes the Rental System class.
    root.mainloop()#Starts the tkinter event loop (root.mainloop()).
