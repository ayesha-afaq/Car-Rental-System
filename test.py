import customtkinter as ctk
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
