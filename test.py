import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import Toplevel

def open_calendar():
    def get_date():
        selected_date = cal.get_date()
        print(f"Selected Date: {selected_date}")
        date_label.configure(text=f"Selected: {selected_date}")
        top.destroy()

    top = Toplevel(root)
    top.title("Select Date")

    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    ctk.CTkButton(top, text="OK", command=get_date).pack(pady=10)



ctk.CTkButton(root, text="Pick a Date", command=open_calendar).pack(pady=20)
date_label = ctk.CTkLabel(root, text="No date selected")
date_label.pack(pady=10)

root.mainloop()
import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow
import os

app = ctk.CTk()
app.title("Custom Icon Example")


# Method 1: Using .ico file (Best for Windows)
try:
    app.iconbitmap("my_icon.ico")  # Works best on Windows
except:
    # Method 2: Using PNG with PIL (Cross-platform)
    try:
        img = Image.open("my car.png")  # Can be .png/.jpg
        icon = ImageTk.PhotoImage(img)
        app.wm_iconphoto(True, icon)
    except Exception as e:
        print(f"Icon not loaded: {e}")

app.mainloop()
