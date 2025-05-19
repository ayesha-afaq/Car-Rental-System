import pyodbc,sys,customtkinter as ctk
from customtkinter import CTkLabel,CTkButton,CTkEntry,CTkFrame,CTkToplevel
from CTkTable import CTkTable
from tkcalendar import Calendar
from tkinter import Toplevel,messagebox
import tkinter as tk
from decimal import Decimal,InvalidOperation
from datetime import datetime, date
import pandas as pd
from abc import ABC,abstractmethod

# sets apperance theme for program
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# Import Connection string to connect to database file
from ConnectionString import connection_string_ayesha


class DuplicateEntryError(Exception):
   def __init__(self, field_name, value):
      super().__init__(f"{field_name.capitalize()} '{value}' already exists.")
        
class InvalidEntry(Exception):
   def __init__(self,msg):
      super().__init__(msg)
 


def messagebox(title, message,error=False,button='ok'):
    
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
         # CONNECTING TO DATABASE
         self.connection=pyodbc.connect(connection_string_ayesha)
         
      except Exception as e:
         # If connection fails, show error message and exit
         root = tk.Tk()
         root.withdraw()  
         tk.messagebox.showerror('Connection Error','please check your database connection and try again')
         sys.exit(1)
      else:
         self.connection.autocommit=True
         self.cursor=self.connection.cursor()

   def set_tablename(self,new_name):
      self.TableName=new_name

   def insert(self,*args):
      #INSERTING NEW DATA INTO TABLE
      try:
         if self.TableName=='Users':
            self.cursor.execute(f"INSERT INTO {self.TableName} (USER_NAME,NAME, PASSWORD, BALANCE,ADDRESS) VALUES (?, ?, ?, ?, ?)",(args[0], args[1], args[2],args[3],args[4]))
         elif self.TableName=='Cars':
            self.cursor.execute(f"INSERT INTO {self.TableName} (CAR_ID, BRAND, MODEL, PricePerDay_$, SeatingCapacity,RESERVATIONSTATUS) VALUES (?, ?, ?, ?, ?, ?)",(args[0], args[1], args[2],args[3],args[4],args[5]))
         elif self.TableName=='RentalHistory':
            self.cursor.execute(f"INSERT INTO {self.TableName} (USER_NAME, CAR_ID, START_DATE, END_DATE,RENTAL_AMOUNT) VALUES (?, ?, ?, ?,?)",(args[0], args[1], args[2],args[3],args[4]))
      except pyodbc.ProgrammingError as e:
         messagebox(title='Error',message=f'{e}',error=True) 
      except pyodbc.IntegrityError as e:
         messagebox(title='Error',message=f'{e}',error=True)
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)
         
   def fetch(self,operation,*args):
      #FETCHING DATA FROM TABLE FOR DIFFERENT OPERATIONS
      try:
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
               self.cursor.execute(f"SELECT TOP 1 END_DATE FROM {self.TableName} WHERE CAR_ID='{args[0]}' ORDER BY Rental_ID DESC")
               return self.cursor.fetchone()
         elif self.TableName=="Admin":
            if operation=="check_admin":
               self.cursor.execute(f"SELECT * FROM {self.TableName} WHERE ADMIN_NAME='{args[0]}' AND PASSWORD='{args[1]}'")
               return self.cursor.fetchone()
      except pyodbc.ProgrammingError as e:
         messagebox(title='Error',message=f'{e}',error=True) 
      except pyodbc.IntegrityError as e:
         messagebox(title='Error',message=f'{e}',error=True)
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)

   def update(self,operation,*args):
      #UPDATING DATA IN TABLE FOR DIFFERENT OPERATIONS
      try:
         if self.TableName=='Users':
            if operation=="update_balance":
               self.cursor.execute(f"UPDATE {self.TableName} SET BALANCE={Decimal(args[1])} WHERE USER_NAME='{args[0]}'")
            elif operation=="update_password":
               self.cursor.execute(f"UPDATE {self.TableName} SET PASSWORD='{args[0]}' WHERE USER_NAME='{args[1]}'")
            elif operation=="update_carid":
               self.cursor.execute(f"UPDATE {self.TableName} SET CAR_ID = ? WHERE USER_NAME = ?",(args[1], args[0]))
         elif self.TableName=='Admin':
            if operation=="update_password":
               self.cursor.execute(f"UPDATE {self.TableName} SET PASSWORD='{args[0]}' WHERE ADMIN_NAME='{args[1]}'")
         elif self.TableName=='Cars':
            if operation=="update_rented":
               self.cursor.execute(f"UPDATE {self.TableName} SET ReservationStatus='{args[1]}' WHERE CAR_ID='{args[0]}'")
      except pyodbc.ProgrammingError as e:
         messagebox(title='Error',message=f'{e}',error=True) 
      except pyodbc.IntegrityError as e:
         messagebox(title='Error',message=f'{e}',error=True)
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)   

   def delete(self,operation,window,*args):
      #DELETING CARS
      if self.TableName=='Cars':
         if operation=="delete_car":
            try:
               result=self.fetch('CheckCarId',args[0])
               if result==None:
                  raise InvalidEntry('Invalid CarID')
               else:
                  self.cursor.execute(f"DELETE FROM {self.TableName} WHERE CAR_ID='{args[0]}'")

            except InvalidEntry as e:
               messagebox(title='Error',message=f'{e}',error=True)
            except pyodbc.ProgrammingError as e:
               messagebox(title='Error',message=f'{e}',error=True) 
            except pyodbc.IntegrityError as e:
               messagebox(title='Error',message=f'{e}',error=True)
            except Exception as e:
               messagebox(title='Error',message=f'{e}',error=True)

            else:
               messagebox(title='Success',message='Car removed successfully!')
               window.destroy()


   def print_table(self,operation):

      def print_table_window(w_title,query):
         try:
               # Create main window
               table_window= ctk.CTk()
               table_window.geometry("800x600")
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
            window=print_table_window(w_title='Car Options',query=f"SELECT * FROM {self.TableName} WHERE RESERVATIONSTATUS='UNRESERVED'")
            window.mainloop()

         
         elif operation=='delete_car':

            window=print_table_window(w_title='Car Options',query=f"SELECT Car_ID, MODEL FROM {self.TableName} WHERE ReservationStatus ='UNRESERVED'")

            id=CTkEntry(master=window,placeholder_text='Car ID')
            id.pack(padx=10,pady=10)
               
            CTkButton(master=window,text='ENTER',command=lambda: self.delete('delete_car',window,(id.get()))).pack(pady=10)

            window.mainloop()
            
         elif operation=='reservedcars':
            window=print_table_window(w_title='Reserved Cars',query=f"SELECT * FROM {self.TableName} WHERE ReservationStatus ='RESERVED' ")
            window.mainloop()
      

      elif self.TableName=='RentalHistory':
         window=print_table_window(w_title='Rental History',query=f"SELECT * FROM {self.TableName} ")
         window.mainloop()

               

class Account(ABC):

   def ChangePassword(self,account_type,username):
     
      # new window for password entry
      change_pass_window = ctk.CTk()  
      change_pass_window.title('Change Password')
      change_pass_window.geometry('400x300')
      
      frame = CTkFrame(master=change_pass_window)
      frame.pack(pady=20, padx=20, fill="both", expand=True)
      
      CTkLabel(frame, text="Enter New Password:").pack(pady=10)
      password_entry = CTkEntry(frame, show="*")
      password_entry.pack(pady=10)
      
      def update_password():
         new_password = password_entry.get()
         strength_score = 0
         if not new_password:
               messagebox('Error', 'Password cannot be empty', error=True)
               return
         if len(new_password) > 6:
            strength_score += 1
         if any(char.isdigit() for char in new_password):
            strength_score += 1
         if any(char.isupper() for char in new_password):
            strength_score += 1
         if any(char.islower() for char in new_password):
            strength_score += 1
         if any(char in "!@#$%^&*()-_+=<>?[]|~`" for char in new_password):
            strength_score += 1
         if strength_score < 3:
            messagebox('Error', 'Password is not strong enough', error=True)
            return
               
         try:
               if account_type == 'Admin':
                  # sets tablename to admin
                  self.db.TableName = "Admin"
                  # update password to database
                  self.db.update("update_password", new_password, username)
               elif account_type == 'Users':
                  # sets tablename to user
                  self.db.TableName = "Users"
                  # update password to database
                  self.db.update("update_password", new_password, username)
                  
               
         except Exception as e:
               messagebox('Error', f'Failed to change password: {str(e)}', error=True)
         else:
            messagebox('Success', 'Password changed successfully!')
            change_pass_window.destroy()

      CTkButton(frame, text="Change Password", command=update_password).pack(pady=20)
      CTkButton(frame, text="Cancel", command=change_pass_window.destroy).pack(pady=10)
      
      change_pass_window.mainloop()


   def back_home(self,destroy_window,deiconify_window):
      try:
         # shows the window again
         deiconify_window.deiconify()
         # completely destroys the window
         destroy_window.destroy()
      except:
         messagebox('Error','Unknown Error Occurred',error=True,button='ok')


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
      ##Instantiates the Record Management class
      self.db=RecordManagement("Cars")
      self.Add_Car_Window()

   def Add_Car_Window(self):
      # new window for taking input car info from user
      car_window=ctk.CTk()
      self.car_window=car_window
      self.car_window.title('Add Car')
      self.car_window.geometry('450x450')
      self.car_Frame=CTkFrame(self.car_window, width=500, height=500)
      self.car_Frame.pack(pady=40)

      ## presents the car id format
      CTkLabel(master=self.car_window,text='Id Format: CR-brand first 3 letters + model\n e.g: bmwM4').pack(pady=10)
      # car id input
      CarID=CTkEntry(master=self.car_Frame,placeholder_text='Enter Car ID',corner_radius=10,fg_color='blue')
      CarID.pack(pady=10)
      # car brand input
      brand=CTkEntry(master=self.car_Frame,placeholder_text='Enter Brand',corner_radius=10,fg_color='blue')
      brand.pack(pady=10)
      # car model input
      model=CTkEntry(master=self.car_Frame,placeholder_text='Enter Model',corner_radius=10,fg_color='blue')
      model.pack(pady=10)
      # car price per day input
      priceperday=CTkEntry(master=self.car_Frame,placeholder_text='Enter price per day in $ (numeric)',corner_radius=10,fg_color='blue')
      priceperday.pack(pady=10)
      # car seating capacity input
      Seating_Capacity=CTkEntry(master=self.car_Frame,placeholder_text='Enter Seating Capacity (numeric)',corner_radius=10,fg_color='blue')
      Seating_Capacity.pack(pady=10)

      # add car to database
      CTkButton(master=self.car_Frame,text='Add Car',command=lambda: self.AddCar(CarID.get(),brand.get(),model.get(),priceperday.get(),Seating_Capacity.get(),self.car_window),corner_radius=10,fg_color='blue').pack(pady=10)
      
      car_window.mainloop()

   def AddCar(self,CarID,Brand,Model,Priceperday,SeatingCap,window):
         # initializes the car attributes
         self.CarId=CarID
         self.Brand=Brand
         self.Model=Model
         self.reservationstatus='UNRESERVED'
      

         try:
            #converts to numeric value
            self.Priceperday=float(Priceperday)
            self.SeatingCapacity=int(SeatingCap)
         except Exception:
            messagebox(title='Error',message=f'Invalid Price or Seating Capacity',error=True)
         
         else:

            try:

               if len(self.CarId)>=3:
                  if self.CarId== f'CR-{self.Brand[0:3]}{self.Model}':
                     result=self.db.fetch('CheckCarId',self.CarId)
                     if result==None:
                           # adds car to database if all entries valid
                           self.db.insert(self.CarId,self.Brand,self.Model,self.Priceperday,self.SeatingCapacity,self.reservationstatus)
                     else:
                           # if car id entered already exists
                           raise DuplicateEntryError('Car ID',self.CarId)
                  else:
                     raise InvalidEntry('CarID is NOt Accurate!')
                  
            

               elif len(self.CarId)<3:

                  if self.CarId==f'CR-{self.CarId}{self.Model}':
                     result=self.db.fetch('CheckCarId',self.CarId)
                     if result==None:
                           # adds car to database if all entries valid
                           self.db.insert(self.CarId,self.Brand,self.Model,self.Priceperday,self.SeatingCapacity,self.reservationstatus)
                     else:
                           # if car id entered already exists
                           raise DuplicateEntryError('Car ID',self.CarId)
                  else:
                     raise InvalidEntry('CarID is NOt Accurate!')

                  
            except InvalidEntry as e:
               messagebox(title='Invalid Entry',message=f'{e}',error=True)
            except DuplicateEntryError as e:
               messagebox(title='Invalid Entry',message=f'{e}',error=True)
            except Exception as e:
               messagebox(title='Error',message=f'{e}',error=True)

            else:
               messagebox(title='Success',message='Car Successfully Added!')
               window.destroy()

            

      
class User(Account):
   def __init__(self,main_window):
      # Withdraws main program window
      main_window.withdraw()
      #MAIN WINDOW FOR USER ACCOUNT
      self.db=RecordManagement("Users")
      self.username, self.name, self.password, self.balance, self.address, self.carid = (None,) * 6
      user_window=ctk.CTk()
      self.user_window=user_window
      self.user_window.title('User Portal')
      self.user_window.geometry('450x450')
      self.user_Frame=CTkFrame(user_window, width=500, height=500)
      self.user_Frame.pack(pady=40)
      CTkButton(master=self.user_Frame,text='SIGN UP',command=lambda: self.CreateUserWindow(),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_Frame,text='LOG IN',command=lambda: self.LoginWindow(main_window=main_window),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_Frame,text='CANCEL',command=lambda: self.back_home(destroy_window=self.user_window,deiconify_window=main_window),corner_radius=10,fg_color='blue').pack(pady=10)
      user_window.mainloop()
     
   def view_balance(self):
      #DISPLAYING BALANCE
      view_balance_window=ctk.CTk()
      self.view_balance_window=view_balance_window
      self.view_balance_window.title('Account Balance')
      self.view_balance_window.geometry('300x200')
      self.view_balance_window_Frame=CTkFrame(view_balance_window, width=500, height=500)
      self.view_balance_window_Frame.pack(pady=40)
      
      balancetxt=CTkLabel(master=self.view_balance_window_Frame,text=f"Your Balance is :{self.balance}")
      balancetxt.pack(pady=10)
      view_balance_window.mainloop()

  
   def login(self, username, password,main_window):
      #FETCHING USER DETAILS FROM DATABASE IF IT EXISTS
      result = self.db.fetch('login', username, password)

      if result is None:
         messagebox('Login Failed', 'Invalid Username or Password', error=True)
         return
      else:
         #SETTING USER DETAILS
         self.name, self.username, self.password, self.balance, self.address, self.carid = result[:6]


         #  Destroy the login window here
         if hasattr(self, 'login_window'):
            self.login_window.destroy()

         # Show main user operations window
         self.ShowOperations(main_window)

      
   def LoginWindow(self,main_window):

      # withdraws the initial user window
      self.user_window.withdraw()

      #LOGIN WINDOW FOR USER ACCOUNT
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

      CTkButton(master=self.login_Frame,text='LOG IN',command=lambda: self.login(user_name.get(), password.get(),main_window=main_window),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.login_Frame,text='CANCEL',command=lambda: self.back_home(destroy_window=self.login_window,deiconify_window=self.user_window),corner_radius=10,fg_color='blue').pack(pady=10)
      
      login_window.mainloop()


   def ShowOperations(self,main_window):
      #withdraws main window of program
      main_window.withdraw()
      #OPERATIONS WINDOW FOR USER ACCOUNT
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
      CTkButton(master=self.user_frame,text='CHANGE PASSWORD',command= lambda: self.ChangePassword(account_type='Users',username=self.username),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.user_frame,text='LOG OUT',command=lambda :self.back_home(destroy_window=self.user_window,deiconify_window=main_window),corner_radius=10,fg_color='blue').pack(pady=10)

      user_window.mainloop()

   def update_balance_ui(self):
      #UPDATE BALANCE WINDOW
      update_balance_window=ctk.CTk()
      self.update_balance_window=update_balance_window
      self.update_balance_window.title('Account Balance')
      self.update_balance_window.geometry('450x450')
      self.update_balance_window_Frame=CTkFrame(update_balance_window, width=500, height=500)
      self.update_balance_window_Frame.pack(pady=40)
     
      balancetxt=CTkLabel(master=self.update_balance_window_Frame,text=f"Enter the amount to be added to your balance :")
      amount=CTkEntry(master=self.update_balance_window_Frame,placeholder_text='Enter amount',corner_radius=10,fg_color='blue')
      
      balancetxt.pack(pady=10)
      amount.pack(pady=10)

      
      balancelabel=CTkLabel(master=self.update_balance_window_Frame,text=f"Your Current Balance is :{self.balance}")
      CTkButton(master=self.update_balance_window_Frame,text='Add Amount',command=lambda: self.update_balance(amount.get(),balancelabel),corner_radius=10,fg_color='blue').pack(pady=10)
      balancelabel.pack(pady=10)
      update_balance_window.mainloop()

   def update_balance(self,amount,balancelabel):
      #UPDATE BALANCE FUNCTION
      try:
         #ONLY NUMERIC VALUES ALLOWED , THE USER CAN BOTH ADD AND WITHDRAW AMOUNT, IN ORDER TO WITHDRAW THE USER HAS TO ENTER A NEGATIVE VALUE
         self.balance+=Decimal(amount)
         self.db.set_tablename("Users")
         #UPDATE THE BALANCE IN DATABASE
         self.db.update("update_balance",self.username,self.balance)
         balancelabel.configure(text=f"Your Current Balance is :{self.balance}")
      except InvalidOperation:
         messagebox('Error','enter a number' ,error=True)
         
      
      
   def CreateUser(self,name,username,password,balance,address):
      #CREATE USER FUNCTION
      self.db.set_tablename("Users")
      existing = self.db.fetch('check_user',username)
      strength_score = 0
      try:
          #CHCEKING IF ALL FIELDS ARE FILLED
         if username=='' or password=='' or name=='' or balance=='' or address=='':
            raise InvalidEntry('Fill in all fields')
         #CHECKING IF USERNAME ALREADY EXISTS
         if existing:
            raise DuplicateEntryError("Username", username)
        
         if len(password) > 6:
            strength_score += 1
         if any(char.isdigit() for char in password):
            strength_score += 1
         if any(char.isupper() for char in password):
            strength_score += 1
         if any(char.islower() for char in password):
            strength_score += 1
         if any(char in "!@#$%^&*()-_+=<>?[]|~`" for char in password):
            strength_score += 1
         if strength_score < 3:
            messagebox('Error', 'Password is not strong enough', error=True)
            return
         #CHECKING IF BALANCE IS NUMERIC
         balance = float(balance)
         self.db.insert(username,name,password,balance,address)
         
      except DuplicateEntryError as e:
         messagebox('Error',f'{e}',error=True)
         return
      except ValueError:
         messagebox('Error','enter a valid amount',error=True)
         return
      except pyodbc.ProgrammingError:
         messagebox('Error','enter a valid amount',error=True)
         return
      except InvalidEntry as e:
         messagebox(title='Invalid Entry',message=f'{e}',error=True)
         return
      else:
         #USER CREATED SUCCESSFULLY
         self.username=username
         self.name=name
         self.password=password
         self.balance=balance
         self.address=address
         messagebox('Success','User Created Successfully please login to continue')
         self.create_user_window.destroy()

   def CreateUserWindow(self):
      # withdraws the initial user window
      self.user_window.withdraw()
      #CREATE USER WINDOW
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
      
      CTkButton(master=self.create_user_Frame,text='CANCEL',command=lambda:self.back_home(destroy_window=self.create_user_window,deiconify_window=self.user_window),corner_radius=10,fg_color='blue').pack(pady=10)
      
      create_user_window.mainloop()

   def rent_car_window(self):
      #RENT CAR WINDOW
      self.db.set_tablename("Users")
      #CHECKING IF USER HAS ALREADY RENTED A CAR
      if self.carid!=None:
         messagebox('Error','You have already rented a car',error=True)
         return
      else:
         #CHECKING IF ANY CARS ARE AVAILABLE FOR RENT
         self.db.set_tablename("Cars")
         result=self.db.fetch('rentcar')
         if result==[]:
            messagebox('Error','No Cars Available for Rent',error=True)
            return
      rent_car_window=ctk.CTk()
      self.rent_car_window=rent_car_window
      self.rent_car_window.title('Rent Car')
      self.rent_car_window.geometry('450x450')
      self.rent_car_Frame=CTkFrame(rent_car_window, width=500, height=500)
      self.rent_car_Frame.pack(pady=40)
      #SHOWS ALL CARS AVAILABLE FOR RENT
      CTkButton(master=self.rent_car_Frame,text='View Cars',command=lambda: self.db.print_table(operation='rentcar'),corner_radius=10,fg_color='blue').pack(pady=10)
      car_id=CTkEntry(master=self.rent_car_Frame,placeholder_text='Enter the car id',corner_radius=10,fg_color='blue')
      car_id.pack(pady=10)
      selected_data = {"startdate": None, "enddate": None}
      # CALENDAR FOR START DATE AND END DATE
      def open_calendar(date_type):
         def get_date():
            # Get the selected date from the calendar and update the label
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
      
      rent_car_window.mainloop()
   

   def rent_car(self,car_id,start_date,end_date):
      #RENT CAR FUNCTION
      try:  
          #CHECKING IF USER HAS ALREADY RENTED A CAR  
         if self.carid!=None:
            messagebox('Error','You have already rented a car',error=True)
            return
         #CHECKING IF ALL FIELDS ARE FILLED
         if start_date==None or end_date==None or car_id=='':
            raise InvalidEntry('Please fill in all fields')
         self.db.set_tablename("Cars")
         result=self.db.fetch('CheckCarId',car_id)
         #CHECKING IF CAR ID EXISTS
         if result==None:
            raise ValueError('Car ID does not exist')  
         self.db.set_tablename("Cars")
         rented=self.db.fetch('checkrented',car_id)
         #CHECKING IF CAR IS ALREADY RENTED
         if rented[0]=='RESERVED':
            messagebox('Error','Car is already rented',error=True)
            return
         result=self.db.fetch('check price',car_id)
         #CALCULATING TOTAL RENTAL AMOUNT
         price=Decimal(result[0])
         start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
         end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
         #CHECKING IF START DATE AND END DATE ARE VALID
         if start_dt > end_dt:
               messagebox('Error', 'Start date cannot be after end date', error=True)
               return
         if start_dt != datetime.today().date():
               messagebox('Error', 'Reservation possible on day to day basis only', error=True)
               return
         rental_days = (end_dt - start_dt).days + 1 
         total_amount = price * Decimal(rental_days)
         #CHECKING IF TOTAL AMOUNT IS GREATER THAN BALANCE
         if total_amount>self.balance:
            messagebox('Error','Insufficient Balance',error=True)
            return
      except InvalidEntry as e:
         messagebox(title='Invalid Entry',message=f'{e}',error=True)
         return
      except ValueError as e:
         messagebox('Error',f'{e}',error=True)
         return
      else:
         #IF ALL CHECKS PASS, UPDATE THE DATABASE AND RENT THE CAR
         self.db.update('update_rented',car_id,'RESERVED')
         self.db.set_tablename("Users")
         self.balance=self.balance-total_amount
         self.db.update("update_balance",self.username,self.balance)
         self.carid=car_id
         self.db.update("update_carid",self.username,self.carid)

         ## Instantiates the Rental History class
         self.rentalhistory=RentalHistory(car_id=car_id,start_date=start_date,end_date=end_date,rental_amount=total_amount,userid=self.username)
         ## adds info to rental history
         self.rentalhistory.add_rental()
         messagebox('Success','Car Rented Successfully')

   def return_car(self):
      #RETURN CAR FUNCTION
      try:
         #CHECKING IF USER HAS RENTED A CAR
         if self.carid==None:
            raise InvalidEntry('You have not rented any car')
         self.db.set_tablename("Users")
         #UNRESERVING THE CAR
         self.db.update('update_carid',self.username,None)
         self.db.set_tablename("Cars")
         self.db.update('update_rented',self.carid,'UNRESERVED')
         self.db.set_tablename("RentalHistory")
         end_date=self.db.fetch('check_enddate',self.carid)

         end_date_str = end_date[0]
         end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d').date()
      except InvalidEntry as e:
         messagebox(title='Invalid Entry',message=f'{e}',error=True)
         return
      #CHECKING IF THE CAR IS RETURNED LATE
      #IF THE CAR IS RETURNED LATE, CALCULATE THE EXTRA AMOUNT
      #AND DEDUCT IT FROM THE BALANCE
      #IF THE CAR IS RETURNED ON TIME, JUST UNRESERVE IT
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
        


class RentalHistory:
   '''Maintains Rental History for each user'''

   def __init__(self,car_id=None,start_date=None,end_date=None,rental_amount=None,userid=None):
      self.car_id=car_id
      self.start_date=start_date
      self.end_date=end_date
      self.rental_amount=rental_amount
      self.userid=userid
      # Instantiates the record management class
      self.db=RecordManagement('RentalHistory')
   
   def add_rental(self):
      '''Adds rental history info to database'''
      try:
         # inserts data
         self.db.insert(self.userid,self.car_id,self.start_date,self.end_date,self.rental_amount)
      except Exception as e:
         messagebox('Error',e,error=True)


class Admin(Account):
   def __init__(self,main_window):
      # Withdraws the main program window
      main_window.withdraw()
      # LOGIN WINDOW FOR ADMIN ACCOUNT
      admin_login_window=ctk.CTk()
      self.admin_login_window=admin_login_window
      self.admin_login_window.title('Login Admin Account')
      self.admin_login_window.geometry('450x450')
      self.admin_login_Frame=CTkFrame(admin_login_window, width=500, height=500)
      self.admin_login_Frame.pack(pady=40)

      #Instantiates the Record Management class
      self.db=RecordManagement('Admin')

      # Username Input
      user_name=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Username',corner_radius=10,fg_color='blue')
      user_name.pack(pady=10)
      
      #Password Input
      password=CTkEntry(master=self.admin_login_Frame,placeholder_text='Enter your Password',corner_radius=10,fg_color='blue')
      password.pack(pady=10)

      #Login Button
      CTkButton(master=self.admin_login_Frame,text='LOGIN',command=lambda: self.ShowOperations(user_name.get(),password.get(),main_window=main_window),corner_radius=10,fg_color='blue').pack(pady=20)
      # Cancel Button
      CTkButton(master=self.admin_login_Frame,text='CANCEL',command=lambda: self.back_home(destroy_window=self.admin_login_window,deiconify_window=main_window),corner_radius=10,fg_color='blue').pack(pady=20)
      
      admin_login_window.mainloop()


   def ShowOperations(self,user_name,password,main_window):
      # sets table name to admin for record management
      self.db.TableName='Admin'
      
      #checks if credentials are valid
      result=self.db.fetch("check_admin",user_name,password)
      if result==None:
         messagebox('Login Failed','Invalid Username or Password',error=True)
         return
      else:
         # destroys the login window if present
         if hasattr(self, 'admin_login_window'):
            self.admin_login_window.destroy()

         #withdraw the main window of program
         main_window.withdraw()

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
         CTkButton(master=self.admin_frame,text='CHANGE PASSWORD',command= lambda: self.ChangePassword(account_type='Admin',username=user_name),corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='VIEW COMPLETE RENTAL HISTORY',command=self.print_comp_rental_history,corner_radius=10,fg_color='blue').pack(pady=10)
         CTkButton(master=self.admin_frame,text='BACK TO HOME PAGE',command=lambda: self.back_home(destroy_window=self.admin_window,deiconify_window=main_window),corner_radius=10,fg_color='blue').pack(pady=10)

         admin_window.mainloop()

   def remove_car(self):
      '''Removes car from database'''
      try:
         #sets tablename to car for record management
         self.db.TableName='Cars'
         #show table for cars that can be removed
         self.db.print_table(operation='delete_car')
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)

   def print_user_rentals(self):
      try:
         #sets tablename to user for record management
         self.db.TableName='Users'
         # show table for user rentals
         self.db.print_table(operation='rentals')
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)
         
   def print_currently_reserved_cars(self):
      try:
         #sets tablename to car for record management
         self.db.TableName='Cars'
         # show table for currently reserved cars
         self.db.print_table(operation='reservedcars')
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)

   def print_comp_rental_history(self):
      try:
         #sets tablename to rental history for record management
         self.db.TableName='RentalHistory'
         # show table of complete rental history
         self.db.print_table(operation='rentalhistory')
      except Exception as e:
         messagebox(title='Error',message=f'{e}',error=True)

   

class Rental_System:
   
   def __init__(self,root):
      '''Initializes the main window of program'''
      self.root=root
      self.root.title('CAR RENTAL SYSTEM')
      self.root.geometry('500x500')

      # HEADER 1
      header=CTkLabel(
         self.root,
         width=10,
         corner_radius=10,
         text='WELCOME TO THE CAR RENTAL SYSTEM\n',
         font=("Times New Roman", 20)).pack(pady=20)
      # HEADER 2
      header2=CTkLabel(
         self.root,
         width=10,
         corner_radius=10,
         text='\nPlease Choose Your Account Type',
         font=("Arial", 16)).pack(pady=10)
         
      self.menu_frame =CTkFrame(root, width=500, height=500)
      self.menu_frame.pack(pady=40)

      # OPTIONS TO SELECT ACCOUNT TYPE OR EXIT SYSTEM
      CTkButton(master=self.menu_frame,text='USER ACCOUNT',command=lambda: User(main_window=self.root),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='ADMINISTRATOR',command=lambda: Admin(main_window=self.root),corner_radius=10,fg_color='blue').pack(pady=10)
      CTkButton(master=self.menu_frame,text='EXIT SYSTEM',command=self.destroy_window,corner_radius=10,fg_color='blue').pack(pady=10)
   
   def destroy_window(self):
      #EXITS THE SYSTEM
      self.root.quit()    
      self.root.destroy()



##____START POINT____##
root=ctk.CTk()
app=Rental_System(root)
root.mainloop()

