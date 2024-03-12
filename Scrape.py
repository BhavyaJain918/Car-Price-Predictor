from bs4 import BeautifulSoup
from tkinter import ttk
import mysql.connector
import tkinter as tk
import requests
import datetime

mydb = mysql.connector.connect(host = "localhost" , user = "" , passwd = "" , database = "Scrape")
myc = mydb.cursor()

cars = []
brands = []

url = "https://www.teoalida.com/cardatabase/list-of-cars-in-india/"
get_url = requests.get(url)

soup = BeautifulSoup(get_url.text , "html.parser")
for model in soup.find_all("summary" , class_ = "wp-block-themeisle-blocks-accordion-item__title")[:-7]:
    brands.append(model.h6.text)

for names in soup.find_all("div" , class_ = "wp-block-themeisle-blocks-accordion-item__content")[:-7]:
    cars.append(names.p.text)

class InvalidData(Exception):
    pass

def purchase_month():
    month = []
    start = int(datetime.datetime.today().strftime("%m")) 
    for i in range(start , 13):
            if i < 10:
                month.append('0' + str(i))
            else:
                month.append(str(i))
    return month

def car_model():
    ind = make_en.current()
    splitted = cars[ind].split(',')
    return splitted

def refresh():
    model_en.configure(values = ()) 
    index = make_en.current()
    new_car = cars[index].split(',')  
    model_en["values"] = new_car 
    model_en.current(0)

def submit(win , reg , engine , chassis , pur_month , pur_year , fuel , make , model):
    register = reg.get()
    eng_num = engine.get()
    ch_num = chassis.get()
    fuel_v = fuel.get()
    mon = pur_month.get()
    year = pur_year.get()
    make_v = make.get()
    model_v = model.get()

    date = mon + '-' + year

    try:
        if register == '' or eng_num == '' or ch_num == '' or fuel_v == '':
            raise InvalidData
        myc.execute("INSERT INTO Vehicle VALUES (%s , %s , %s , %s , %s , %s , %s)" , (register , eng_num , ch_num , fuel_v , date , make_v , model_v))
        mydb.commit()
        lab = ttk.Label(win , text = "Entry Successful !")
        lab.grid(row = 6 , column = 1 , padx = 40 , pady = 10 , sticky = 'E')
        win.after(2000 , lambda: lab.destroy())
    except mysql.connector.errors.DataError:
        lab = ttk.Label(win , text = "Data Too Long !")
        lab.grid(row = 6 , column = 1 , padx = 40 , pady = 10 , sticky = 'E')
        win.after(2000 , lambda: lab.destroy())
    except mysql.connector.errors.IntegrityError:
        lab = ttk.Label(win , text = "Data Exists !")
        lab.grid(row = 6 , column = 1 , padx = 40 , pady = 10 , sticky = 'E')
        win.after(2000 , lambda: lab.destroy())
    except InvalidData:
        lab = ttk.Label(win , text = "Data Invalid !")
        lab.grid(row = 6 , column = 1 , padx = 40 , pady = 10 , sticky = 'E')
        win.after(2000 , lambda: lab.destroy())





root = tk.Tk()
fr = tk.Frame()
root.title("Vehicle Details") 
root.resizable(False , False)

reg = ttk.Label(root , text = "Registration Number : ")
reg.grid(row = 0 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
reg_en = ttk.Entry(root , width = 40)
reg_en.grid(row = 0 , column = 1 , padx = 10 , pady = 10 , sticky = 'W')

eng = ttk.Label(root , text = "Engine Number : ")
eng.grid(row = 1 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
eng_en = ttk.Entry(root , width = 40)
eng_en.grid(row = 1 , column = 1 , padx = 10 , pady = 10 , sticky = 'W')


chs = ttk.Label(root , text = "Chassis Number : ")
chs.grid(row = 2 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
chs_en = ttk.Entry(root , width = 40)
chs_en.grid(row = 2 , column = 1 , padx = 10, pady = 10 , sticky = 'W')

purchase = ttk.Label(root , text = "Month and Year : ")
purchase.grid(row = 3 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
purchase_en = ttk.Combobox(root , width = 14 , state = "readonly")
purchase_en["values"] = purchase_month()
purchase_en.bind("<<ComboboxSelected>>" , lambda p : root.focus())
purchase_en.current(0)
purchase_en.grid(row = 3 , column = 1 , padx = 10 , pady = 10 , sticky = 'W') 

purchase_year = ttk.Combobox(root , width = 18 , state = "readonly")
purchase_year["values"] = datetime.datetime.today().strftime("%Y")
purchase_year.bind("<<ComboboxSelected>>" , lambda p : root.focus())
purchase_year.current(0)
purchase_year.grid(row = 3 , column = 1 , padx = 10 , pady = 10 , sticky = 'E') 

type = ttk.Label(root , text = "Vehicle Fuel Type : ")
type.grid(row = 4 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
type_en = ttk.Entry(root , width = 40)
type_en.grid(row = 4 , column = 1 , padx = 10 , pady = 10 , sticky = 'W') 


make = ttk.Label(root , text = "Make and Model : ")
make.grid(row = 5 , column = 0 , padx = 10 , pady = 10 , sticky = 'E')
make_en = ttk.Combobox(root , width = 15 , state = "readonly")
make_en["values"] = brands
make_en.bind("<<ComboboxSelected>>" , lambda p : root.focus())
make_en.current(0)
make_en.bind("<<ComboboxSelected>>" , lambda p : refresh() , add = True)
make_en.grid(row = 5 , column = 1 , padx = 10 , pady = 10 , sticky = 'W') 

model_en = ttk.Combobox(root , width = 17 , state = "readonly")
refresh()
model_en.bind("<<ComboboxSelected>>" , lambda p : root.focus())
model_en.grid(row = 5 , column = 1 , padx = 10 , pady = 10 , sticky = 'E') 

button = ttk.Button(root , text = "Submit Details" , command = lambda: submit(root , reg_en , eng_en , chs_en , purchase_en , purchase_year , type_en , make_en , model_en))
button.grid(row = 6 , column = 1 , padx = 10 , pady = 10 , sticky = 'W') 

root.mainloop()