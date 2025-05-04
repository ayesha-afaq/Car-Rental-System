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
