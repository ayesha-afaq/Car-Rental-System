
import pyodbc
import customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkInputDialog,CTkToplevel
from CTkTable import CTkTable
from tkcalendar import Calendar
from tkinter import Toplevel

from decimal import Decimal,InvalidOperation
from datetime import datetime, date




import pandas as pd
from abc import ABC,abstractmethod

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')



from ConnectionString import connection_string_ayesha

class DuplicateEntryError(Exception):
    def __init__(self, field_name, value):
        super().__init__(f"{field_name.capitalize()} '{value}' already exists.")
        
class InvalidEntry(Exception):
   pass

def messagebox(title, message,error=False,button='ok'):
    ## custom tkinter mAE message box khud sae nhi arha tha tu is liyay yay bnya hAE
   top = CTkToplevel()
   top.title(title)
   top.geometry("300x200")
   top.resizable(False, False)
   if error==True:
        CTkLabel(top,text="⚠️",font=("Arial", 24)).pack(pady=10)
    # Message
   CTkLabel(top, text=message).pack(pady=30)
   if button=='ok':
      # OK button (closes the window)
      CTkButton(top, text="OK", command=top.destroy).pack()
   elif button=='next':
      CTkButton(top, text="Next", command=top.destroy).pack()
   


class RecordManagement:
   def __init__(self,TableName):
      self.TableName=TableName
      try:
         self.connection=pyodbc.connect(connection_string_ayesha)
         print('connected to database')
         
      except Exception as e:
         print('connection error')
         messagebox('Connection Error',e,error=True)
         return
      else:
         self.connection.autocommit=True
         self.cursor=self.connection.cursor()

   def set_tablename(self,new_name):
      self.TableName=new_name

   def insert(self,*args):
      
      if self.TableName=='Users':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (USER_NAME,NAME, PASSWORD, BALANCE,ADDRESS) VALUES (?, ?, ?, ?, ?)",
                           (args[0], args[1], args[2],args[3],args[4]))
     
      elif self.TableName=='Cars':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (CAR_ID, BRAND, MODEL, PricePerDay_$, SeatingCapacity,RESERVATIONSTATUS) VALUES (?, ?, ?, ?, ?, ?)",
                           (args[0], args[1], args[2],args[3],args[4],args[5]))
      elif self.TableName=='RentalHistory':
         self.cursor.execute(
                           f"INSERT INTO {self.TableName} (USER_NAME, CAR_ID, START_DATE, END_DATE,RENTAL_AMOUNT) VALUES (?, ?, ?, ?,?)",
                           (args[0], args[1], args[2],args[3],args[4]))
         
     
         
   def fetch(self,operation,*args):
      if self.TableName=='Users':
         if operation=="login":
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE USER_NAME='{args[0]}' AND PASSWORD='{args[1]}'")
            return self.cursor.fetchone()
         
         elif operation=="balance check":
            self.cursor.execute(f"SELECT BALANCE FROM {self.TableName} WHERE USER_NAME='{args[0]}'")
            return self.cursor.fetchone()
         elif operation=="checkcar":
            self.cursor.execute(f"SELECT CAR_ID FROM {self.TableName} WHERE USER_NAME='{args[0]}'")
            return self.cursor.fetchone()
         elif operation=="check_user":
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE USER_NAME='{args[0]}'")
            return self.cursor.fetchone()
      elif self.TableName=='Cars':
         if operation=="check price":
            self.cursor.execute(f"SELECT PricePerDay_$ FROM {self.TableName} WHERE CAR_ID='{args[0]}'")
            return self.cursor.fetchone()
         elif operation=="checkrented":
            self.cursor.execute(f"SELECT RESERVATIONSTATUS FROM {self.TableName} WHERE CAR_ID='{args[0]}'")
            return self.cursor.fetchone()
         elif operation=="rentcar":
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE ReservationStatus='UNRESERVED'")
            return self.cursor.fetchall()
         elif operation=='CheckCarId':
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE CAR_ID ='{args[0]}'")
            return self.cursor.fetchone()
      elif self.TableName=='RentalHistory':
         if operation=="check_enddate":
            print(args[0])
            print(f"SELECT END_DATE FROM {self.TableName} WHERE CAR_ID='{args[0]}'")
            self.cursor.execute(f"SELECT END_DATE FROM {self.TableName} WHERE CAR_ID='{args[0]}'")
            return self.cursor.fetchone()
      elif self.TableName=="Admin":
         if operation=="check_admin":
            self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE ADMIN_NAME='{args[0]}' AND PASSWORD='{args[1]}'")
            return self.cursor.fetchone()

   def update(self,operation,*args):
      if self.TableName=='Users':
         if operation=="update_balance":
            print(args[0],args[1])
            self.cursor.execute(f"UPDATE {self.TableName} SET BALANCE={Decimal(args[1])} WHERE USER_NAME='{args[0]}'")
         elif operation=="update_password":
            self.cursor.execute(f"UPDATE {self.TableName} SET PASSWORD={args[0]} WHERE USER_NAME='{args[1]}'")
         elif operation=="update_carid":
            # self.cursor.execute(f"UPDATE {self.TableName} SET CAR_ID='{args[1]}' WHERE USER_NAME='{args[0]}'") 
            self.cursor.execute(
                f"UPDATE {self.TableName} SET CAR_ID = ? WHERE USER_NAME = ?",
                (args[1], args[0])
            )
      elif self.TableName=='Admin':
         if operation=="update_password":
            self.cursor.execute(f"UPDATE {self.TableName} SET PASSWORD={args[0]} WHERE ADMIN_NAME='{args[1]}'")
      elif self.TableName=='Cars':
         if operation=="update_rented":
            self.cursor.execute(f"UPDATE {self.TableName} SET ReservationStatus='{args[1]}' WHERE CAR_ID='{args[0]}'")
         
         
      
      

   def delete(self,operation,window,*args):
      if self.TableName=='Cars':
         if operation=="delete_car":
            try:
               self.cursor.execute(f"DELETE FROM {self.TableName} WHERE CAR_ID='{args[0]}'")
            except:
               messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)
            else:
               messagebox(title='Success',message='Car removed successfully!')
               window.destroy()


   def print_table(self,operation):

      def print_table_window(w_title,query):
         try:
               # Create main window
               table_window= ctk.CTk()
               table_window.geometry("800x400")
               table_window.title(w_title)

               # Fetch data without pandas warning
               self.cursor.execute(query)
               columns = [column[0] for column in self.cursor.description]  # Get column names
               data = self.cursor.fetchall()

               if len(data)==0:
                  messagebox(title=w_title,message='Table has NO Entries Yet',button='OK')
               else:

                  # # Convert to format CTkTable needs (list of lists)
                  table_data = [columns] + list(data)

                  # # Create table
                  table = CTkTable(master=table_window, row=len(table_data), column=len(columns), values=table_data)
                  table.pack(expand=True, fill="both", padx=20, pady=20)


                  # # Add some styling
                  table.configure(header_color="#2b2b2b", hover_color="#3a3a3a")

                  return table_window

         except:
               messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)
      
      if self.TableName=="Users":
         if operation=='rentals':
            window=print_table_window(w_title='User Rentals',query=f"SELECT * FROM {self.TableName} WHERE Car_ID IS NOT NULL")
            window.mainloop()
      
      elif self.TableName=="Cars":
         
         if operation=='rentcar':
            window=print_table_window(title='Car Options',query=f"SELECT * FROM {self.TableName} WHERE RESERVATIONSTATUS='UNRESERVED'")
            window.mainloop()

         
         elif operation=='delete_car':

            window=print_table_window(w_title='Car Options',query=f"SELECT Car_ID, MODEL FROM {self.TableName} WHERE ReservationStatus ='UNRESERVED'")

            id=CTkEntry(master=window,placeholder_text='Car ID')
            id.pack(padx=10,pady=10)
               
            CTkButton(master=window,text='ENTER',command=lambda: self.delete('delete_car',window,id.get())).pack(pady=10)

            window.mainloop()
            
         elif operation=='reservedcars':
            window=print_table_window(w_title='Reserved Cars',query=f"SELECT * FROM {self.TableName} WHERE ReservationStatus ='RESERVED' ")
            window.mainloop()
      

      elif self.TableName=='RentalHistory':
         window=print_table_window(w_title='Rental History',query=f"SELECT * FROM {self.TableName} ")
         window.mainloop()

               

class Account(ABC):
      
   def ChangePassword(self,account,username):

      def Change(username,password,window):
         if account=='Admin':
            try:
               self.db.TableName="Admin"
               self.db.update("update_password",password,username)
               messagebox('Success',message='Password Changed Successfully',button='ok')
               window.destroy()
            except:
               messagebox('Error','Unknown Error Occurred',error=True,button='ok')

         elif account=='User':
            try:
               self.db.TableName="Users"
               self.db.update("update_password",password,username)
               messagebox('Success',message='Password Changed Successfully',button='ok')
               window.destroy()
            except:
               messagebox('Error','Unknown Error Occurred',error=True,button='ok')

      change_pass_window=ctk.CTk()
      self.change_pass_window=change_pass_window
      self.change_pass_window.title('Change Password')
      self.change_pass_window.geometry('500x500')
      self.pass_Frame=CTkFrame(master=self.change_pass_window,width=500, height=500)
      self.pass_Frame.pack()
      self.db=RecordManagement(None)
      
      password=CTkEntry(master=self.pass_Frame,placeholder_text='Enter your new password',corner_radius=10,fg_color='blue')
      password.pack(pady=10)
      CTkButton(master=self.pass_Frame,text='Enter',command=lambda: Change(username,password.get(),window=self.change_pass_window)).pack(pady=20)
      self.change_pass_window.mainloop()

   def back_home(self,window):
      try:
         window.destroy()
         print('admin window destroyed')
      except:
         print('unknown error')


   @abstractmethod
   def ShowOperations(self):
      pass
   

class Car:
   def __init__(self):
      self.CarId=None
      self.Brand=None
      self.Model=None
      self.PricePerDay=None
      self.SeatingCapacity=None
      self.reserve=None
      self.db=RecordManagement("Cars")
      self.Add_Car_Window()

   def Add_Car_Window(self):
      car_window=ctk.CTk()
      self.car_window=car_window
      self.car_window.title('Add Car')
      self.car_window.geometry('450x450')
      self.car_Frame=CTkFrame(self.car_window, width=500, height=500)
      self.car_Frame.pack(pady=40)

      CTkLabel(master=self.car_window,text='Id Format: CR-brand first 3 letters + model\n e.g: bmw1989 ').pack(pady=10)

      CarID=CTkEntry(master=self.car_Frame,placeholder_text='Enter Car ID',corner_radius=10,fg_color='blue')
      CarID.pack(pady=10)
      brand=CTkEntry(master=self.car_Frame,placeholder_text='Enter Brand',corner_radius=10,fg_color='blue')
      brand.pack(pady=10)
      model=CTkEntry(master=self.car_Frame,placeholder_text='Enter Model',corner_radius=10,fg_color='blue')
      model.pack(pady=10)
      
      priceperday=CTkEntry(master=self.car_Frame,placeholder_text='Enter price per day in $',corner_radius=10,fg_color='blue')
      priceperday.pack(pady=10)
      Seating_Capacity=CTkEntry(master=self.car_Frame,placeholder_text='Enter Seating Capacity',corner_radius=10,fg_color='blue')
      Seating_Capacity.pack(pady=10)

      
      CTkButton(master=self.car_Frame,text='Add Car',command=lambda: self.AddCar(CarID.get(),brand.get(),model.get(),priceperday.get(),Seating_Capacity.get(),self.car_window),corner_radius=10,fg_color='blue').pack(pady=10)
      
      
      car_window.mainloop()

   def AddCar(self,CarID,Brand,Model,Priceperday,SeatingCap,window):
      self.CarId=CarID
      self.Brand=Brand
      self.Model=Model
      self.Priceperday=Priceperday
      self.SeatingCapacity=SeatingCap
      self.reservationstatus='UNRESERVED'
      try:
         if self.CarId== f'CR-{self.Brand[0:3]}{self.Model}':
            result=self.db.fetch('CheckCarId',self.CarId)
            if result==None:
               self.db.insert(self.CarId,self.Brand,self.Model,self.Priceperday,self.SeatingCapacity,self.reservationstatus)
            else:
               raise DuplicateEntryError('Car ID',self.CarId)
               
         else:
            raise InvalidEntry('CarID is NOt Accurate!')

      except InvalidEntry as e:
         messagebox(title='Invalid Entry',message=f'{e}',error=True)
      except DuplicateEntryError as e:
         messagebox(title='Invalid Entry',message=f'{e}',error=True)
      except:
         messagebox(title='Unknown Error',message='An Unknown Error Occurred',error=True)
      else:
         messagebox(title='Success',message='Car Successfully Added!')
         window.destroy()

      
class User(Account):
   def __init__(self):
      self.db=RecordManagement("Users")
      self.username=None
      self.name=None
      self.password=None
      self.balance=None
      self.address=None
      self.carid=None
      user_window=ctk.CTk()
      self.user_window=user_window
      self.user_window.title('User Portal')
      self.user_window.geometry('450x450')
      self.user_Frame=CTkFrame(user_window, width=500, height=500)
      self.user_Frame.pack(pady=40)
      CTkButton(master=self.user_Frame,text='Sign up',command=lambda: self.CreateUserWindow(),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_Frame,text='Log in',command=lambda: self.LoginWindow(),corner_radius=10,fg_color='blue').pack(pady=10)
      user_window.mainloop()
      #idr user qindow bnegi jismai login , create user ka option hoga , if user clicks on create user then create user ka window khulega wrna login ka
   def view_balance(self):
      view_balance_window=ctk.CTk()
      self.view_balance_window=view_balance_window
     
      self.view_balance_window.title('Account Balance')
      self.view_balance_window.geometry('450x450')
      self.view_balance_window_Frame=CTkFrame(view_balance_window, width=500, height=500)
      self.view_balance_window_Frame.pack(pady=40)
      
      balancetxt=CTkLabel(master=self.view_balance_window_Frame,text=f"Your Balance is :{self.balance}")
      balancetxt.pack(pady=10)
      view_balance_window.mainloop()

  
   def login(self, username, password):
      result = self.db.fetch('login', username, password)

      if result is None:
        messagebox('Login Failed', 'Invalid Username or Password', error=True)
        return
      else:
        messagebox('Login Success', 'Welcome to the Car Rental System :)')
        self.username = result[1]
        self.name = result[0]
        self.password = result[2]
        self.balance = result[3]
        self.address = result[4]
        self.carid = result[5]

        #  Destroy the login window here
        if hasattr(self, 'login_window'):
            self.login_window.destroy()

        # Show main user operations window
        self.ShowOperations()

      
   def LoginWindow(self):
    # Destroy the initial user portal window
    if hasattr(self, 'user_window'):
        self.user_window.destroy()

    login_window = ctk.CTk()
    self.login_window = login_window
    self.login_window.title('Login')
    self.login_window.geometry('450x450')
    self.login_Frame = CTkFrame(login_window, width=500, height=500)
    self.login_Frame.pack(pady=40)

    user_name = CTkEntry(master=self.login_Frame, placeholder_text='Enter your username', corner_radius=10, fg_color='blue')
    user_name.pack(pady=10)

    password = CTkEntry(master=self.login_Frame, placeholder_text='Enter your password', corner_radius=10, fg_color='blue')
    password.pack(pady=10)

    CTkButton(
        master=self.login_Frame,
        text='Log in',
        command=lambda: self.login(user_name.get(), password.get()),
        corner_radius=10,
        fg_color='blue'
    ).pack(pady=10)

    login_window.mainloop()


   def ShowOperations(self):
      ## inme change password ka option bhi rkhna hae jo admin aur user kai liyay same hoga account class sae inherit hoga
      user_window=ctk.CTk()
      self.user_window=user_window
      self.user_window.title('User Portal')
      self.user_window.geometry('450x450')
      self.user_frame =CTkFrame(user_window, width=500, height=500)
      self.user_frame.pack(pady=40)
      CTkButton(master=self.user_frame,text='RENT A CAR',command=self.rent_car_window,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='RETURN CAR',command=self.return_car,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='VIEW BALANCE',command=self.view_balance,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='UPDATE BALANCE',command=self.update_balance_ui,corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='CHANGE PASSWORD',command= lambda: self.ChangePassword(username=self.username,account='User'),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='BACK TO HOME PAGE',command=lambda :self.back_home(self.user_window),corner_radius=10,fg_color='blue').pack(pady=10)

      user_window.mainloop()
   def update_balance_ui(self):
      update_balance_window=ctk.CTk()
      self.update_balance_window=update_balance_window
      self.update_balance_window.title('Account Balance')
      self.update_balance_window.geometry('450x450')
      self.update_balance_window_Frame=CTkFrame(update_balance_window, width=500, height=500)
      self.update_balance_window_Frame.pack(pady=40)
      # self.db=RecordManagement("Users")
      # result=self.db.fetch('balance check',self.username)
      # balancetxt=CTkLabel(master=self.view_balance_window_Frame,text=f"Your Balance is :{result[0]}")
      balancetxt=CTkLabel(master=self.update_balance_window_Frame,text=f"Enter the amount to be added to your balance :")
      amount=CTkEntry(master=self.update_balance_window_Frame,placeholder_text='Enter amount',corner_radius=10,fg_color='blue')
      
      balancetxt.pack(pady=10)
      amount.pack(pady=10)

      ## check lgegea kae amount int mae hai ya nhi 
      balancelabel=CTkLabel(master=self.update_balance_window_Frame,text=f"Your Current Balance is :{self.balance}")
      CTkButton(master=self.update_balance_window_Frame,text='Add Amount',command=lambda: self.update_balance(amount.get(),balancelabel),corner_radius=10,fg_color='blue').pack(pady=10)
      balancelabel.pack(pady=10)
      update_balance_window.mainloop()

   def update_balance(self,amount,balancelabel):
      
      try:
         self.balance+=Decimal(amount)
         self.db.set_tablename("Users")
         
         self.db.update("update_balance",self.username,self.balance)
         balancelabel.configure(text=f"Your Current Balance is :{self.balance}")
      except InvalidOperation:
         messagebox('Error','enter a number' ,error=True)
         
      
      
   def CreateUser(self,name,username,password,balance,address):
      self.db.set_tablename("Users")
      existing = self.db.fetch('check_user',username)
      
      try:
         if existing:
            raise DuplicateEntryError("Username", username)
         self.db.insert(self.username,self.name,self.password,self.balance,self.address)
      except DuplicateEntryError as e:
         messagebox('Error',f'{e}',error=True)
      except pyodbc.ProgrammingError:
         messagebox('Error','enter a valid amount',error=True)
      else:
         self.username=username
         self.name=name
         self.password=password
         self.balance=balance
         self.address=address

   def CreateUserWindow(self):
      create_user_window=ctk.CTk()
      self.create_user_window=create_user_window
      self.create_user_window.title('Create User')
      self.create_user_window.geometry('450x450')
      self.create_user_Frame=CTkFrame(create_user_window, width=500, height=500)
      self.create_user_Frame.pack(pady=40)
      
      
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

   def rent_car_window(self):
      self.db.set_tablename("Users")
      # checkcar=self.db.fetch('checkcar',self.username)
      # if checkcar[0]!=None:
      if self.carid!=None:
         messagebox('Error','You have already rented a car',error=True)
         return
      else:
         self.db.set_tablename("Cars")
         result=self.db.fetch('rentcar')
         print(result)
         if result==[]:
            messagebox('Error','No Cars Available for Rent',error=True)
            return
      rent_car_window=ctk.CTk()
      self.rent_car_window=rent_car_window
      self.rent_car_window.title('Rent Car')
      self.rent_car_window.geometry('450x450')
      self.rent_car_Frame=CTkFrame(rent_car_window, width=500, height=500)
      self.rent_car_Frame.pack(pady=40)
      
      CTkButton(master=self.rent_car_Frame,text='View Cars',command=lambda: self.db.print_table('rentcar'),corner_radius=10,fg_color='blue').pack(pady=10)
      car_id=CTkEntry(master=self.rent_car_Frame,placeholder_text='Enter the car id',corner_radius=10,fg_color='blue')
      car_id.pack(pady=10)
      selected_data = {"startdate": None, "enddate": None}

      def open_calendar(date_type):
         def get_date():
            selected_date = cal.get_date()
            selected_data[date_type] = selected_date
            if date_type == "startdate":
                  start_date_label.configure(text=f"Start Date: {selected_date}")
            elif date_type == "enddate":
                  end_date_label.configure(text=f"End Date: {selected_date}")
            top.destroy()

         top = Toplevel(self.rent_car_window)
         top.title(f"Select {date_type.capitalize()}")

         cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
         cal.pack(pady=10)

         ctk.CTkButton(top, text="OK", command=get_date).pack(pady=10)

     
      CTkButton(master=self.rent_car_Frame,
               text="Pick Start Date",
               command=lambda: open_calendar("startdate")).pack(pady=10)

      start_date_label = CTkLabel(master=self.rent_car_Frame, text="No start date selected")
      start_date_label.pack(pady=5)


      CTkButton(master=self.rent_car_Frame,
               text="Pick End Date",
               command=lambda: open_calendar("enddate")).pack(pady=10)

      end_date_label = CTkLabel(master=self.rent_car_Frame, text="No end date selected")
      end_date_label.pack(pady=5)


      CTkButton(master=self.rent_car_Frame,text='Rent Car',command=lambda:self.rent_car(car_id.get(),selected_data['startdate'],selected_data['enddate']),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.rent_car_Frame,text='Back to User Portal',command=lambda: self.back_home(self.rent_car_window),corner_radius=10,fg_color='blue').pack(pady=10)
      rent_car_window.mainloop()
   

   def rent_car(self,car_id,start_date,end_date):
      
               self.db.set_tablename("Cars")
               rented=self.db.fetch('checkrented',car_id)
               if rented[0]=='RESERVED':
                  messagebox('Error','Car is already rented',error=True)
                  return
               result=self.db.fetch('check price',car_id)
               price=Decimal(result[0])
               
               total_amount=price*(Decimal(end_date[9:])-Decimal(start_date[9:]))
               print(total_amount)
               if total_amount>self.balance:
                  messagebox('Error','Insufficient Balance',error=True)
                  return
               else:
                  
                  self.db.update('update_rented',car_id,'RESERVED')
                  self.db.set_tablename("Users")
                  self.balance=self.balance-total_amount
                  self.db.update("update_balance",self.username,self.balance)
                  self.carid=car_id
                  self.db.update("update_carid",self.username,self.carid)
               
                  self.db.set_tablename("RentalHistory")
                  self.db.insert(self.username,car_id,start_date,end_date,total_amount)
                  messagebox('Success','Car Rented Successfully')

   def return_car(self):
      #carid fetch , car id remove , date chcek if more than money deduct , car unreseve 
      self.db.set_tablename("Users")
   
      self.db.update('update_carid',self.username,None)
      self.db.set_tablename("Cars")
      self.db.update('update_rented',self.carid,'UNRESERVED')
      
      self.db.set_tablename("RentalHistory")
      end_date=self.db.fetch('check_enddate',self.carid)
      print(end_date)
      end_date_str = end_date[0]
      end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d').date()

      if end_date_obj < date.today():
         date_difference = (date.today() - end_date_obj).days
            
      
         self.db.set_tablename("Cars")
         result=self.db.fetch('check price',self.carid)
         price=result[0]
         total_amount=price*date_difference  
         self.db.set_tablename("Users")
         self.db.update("update_balance",self.username,self.balance-total_amount)   
         self.balance=self.balance-total_amount
         self.carid=None
         messagebox('Success',f'Car Returned Successfully\n{total_amount} Amount deducted from your balance')
      else:
         self.carid=None
         messagebox('Success','Car Returned Successfully')
        

   #return late date,insert krne pr try except,gari li nai but return kr rhe ,passchange,gari rent krte v agr aik he screen mai dubara rent, dedeuct krne pr paisy, 



class RentalHistory:

   def __init__(self,car_id=None,start_date=None,end_date=None,rental_amount=None):
      self.car_id=car_id
      self.start_date=start_date
      self.end_date=end_date
      self.rental_amount=rental_amount
      self.db=RecordManagement('RentalHistory')
   
   def add_rental(self):
      try:
         self.db.insert(self.car_id,self.start_date,self.end_date,self.rental_amount)
         messagebox('Success','Rental history record added successfully')
      except Exception as e:
         messagebox('Error',e,error=True)


class Admin(Account):
   def __init__(self):
      admin_login_window=ctk.CTk()
      self.admin_login_window=admin_login_window
      self.admin_login_window.title('Login Admin Account')
      self.admin_login_window.geometry('450x450')
      self.admin_login_Frame=CTkFrame(admin_login_window, width=500, height=500)
      self.admin_login_Frame.pack(pady=40)
      self.db=RecordManagement('Admin')
      
      user_name=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Username',corner_radius=10,fg_color='green')
      user_name.pack(pady=10)
      
      
      password=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Password',corner_radius=10,fg_color='green')
      password.pack(pady=10)
      
      CTkButton(master=self.admin_login_Frame,text='Login',command=lambda: self.ShowOperations(user_name.get(),password.get(),window=admin_login_window),corner_radius=10,fg_color='blue').pack(pady=20)
      admin_login_window.mainloop()


   def ShowOperations(self,user_name,password,window):

      self.db.set_tablename('Admin')
      try:
         self.db.fetch("check_admin",user_name,password)
      except:
         messagebox(title='Login Error',message='Incorrect Username or Password',error=True)
      self.db.set_tablename='Admin'

      result=self.db.fetch("check_admin",user_name,password)
      if result==None:
         messagebox('Login Failed','Invalid Username or Password',error=True)
         return
      else:
         #destroy the login window
         window.destroy()
         # new window to show operations of admin
         admin_window=ctk.CTk()
         self.admin_window=admin_window
         self.admin_window.title('Admin')
         self.admin_window.geometry('450x450')
         self.admin_frame =CTkFrame(admin_window, width=500, height=500)
         self.admin_frame.pack(pady=40)
         CTkButton(master=self.admin_frame,text='ADD CAR',command= lambda: Car(),corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='REMOVE CAR',command=self.remove_car,corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='CURRENTLY RESERVED CARS',command= self.print_currently_reserved_cars,corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='CURRENT RENTALS REPORT',command=self.print_user_rentals,corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='CHANGE PASSWORD',command= lambda: self.ChangePassword(account='Admin',username=user_name),corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='VIEW COMPLETE RENTAL HISTORY',command=self.print_comp_rental_history,corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='BACK TO HOME PAGE',command=lambda: self.back_home(window=self.admin_window),corner_radius=10,fg_color='blue').pack(pady=10)

         admin_window.mainloop()

   def remove_car(self):
      try:
         self.db.TableName='Cars'
         self.db.print_table(operation='delete_car')
      except:
         messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)

   def print_user_rentals(self):
      try:
         self.db.TableName='Users'
         self.db.print_table(operation='rentals')
      except:
         messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)
         
   def print_currently_reserved_cars(self):
      try:
         self.db.TableName='Cars'
         self.db.print_table(operation='reservedcars')
      except:
         messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)

   def print_comp_rental_history(self):
      try:
         self.db.TableName='RentalHistory'
         self.db.print_table(operation='rentalhistory')
      except:
         messagebox(title='Error',message='Unknown Error Occurred.\nPls Try Again',error=True)




   

class Rental_System:
   
   def __init__(self,root):
      self.root=root
      self.root.title('CAR RENTAL SYSTEM')
      self.root.geometry('500x500')
      header=CTkLabel(
         self.root,
         width=10,
         corner_radius=10,
         text='WELCOME TO THE CAR RENTAL SYSTEM\n',
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




root=ctk.CTk()
app=Rental_System(root)
root.mainloop()
