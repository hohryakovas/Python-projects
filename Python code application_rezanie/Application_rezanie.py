from tkinter import *
from tkinter import ttk
import tkinter as tk
import math
root = Tk()
root.title("Расчёт резания")
root.geometry("720x480")

table1 = {"1-50": 15,"51-100": 10,"101-200": 8,"201-300": 6,"301-400": 4}
CalculationData = []
x_plate = 0
y_plate = 0
z_plate = 0


x_detail = 0
y_detail = 0
z_detail = 0

label_thickness = ttk.Label(anchor=W,text="Введите размеры плиты",font="14")
label_thickness.grid(row = 0,column=0)

label_length = ttk.Label(text="Введите длину плиты")
label_length.grid(row = 1,column=0)
entry_length = ttk.Entry()
entry_length.grid(row = 1,column=1)

label_height = ttk.Label(anchor=NW, text="Введите ширину плиты")
label_height.grid(row = 2,column=0)
entry_height = ttk.Entry()
entry_height.grid(row = 2,column=1)

label_thickness = ttk.Label(anchor=W,text="Введите толщину плиты")
label_thickness.grid(row = 3,column=0)
entry_thickness = ttk.Entry()
entry_thickness.grid(row = 3,column=1)

label_thickness = ttk.Label(anchor=W,text="Введите размеры детали",font="14")
label_thickness.grid(row = 4,column=0)

label_length = ttk.Label(text="Введите длину детали")
label_length.grid(row = 5,column=0)
entry_x_detail = ttk.Entry()
entry_x_detail.grid(row = 5,column=1)

label_height = ttk.Label(anchor=NW, text="Введите ширину детали")
label_height.grid(row = 6,column=0)
entry_y_detail = ttk.Entry()
entry_y_detail.grid(row = 6,column=1)

label_thickness = ttk.Label(anchor=W,text="Введите толщину детали")
label_thickness.grid(row = 7,column=0)
entry_z_detail = ttk.Entry()
entry_z_detail.grid(row = 7,column=1)

label_saw_price = ttk.Label(anchor=W,text="Введите цену пилы в USD")
label_saw_price.grid(row = 8,column=0)
entry_saw_price = ttk.Entry()
entry_saw_price.grid(row = 8,column=1)

def show():
    #Длина,ширина,высота плиты
    x_plate = float(entry_length.get())
    y_plate = float(entry_height.get())
    z_plate = float(entry_thickness.get())
    
    #Цена пилы в USD
    saw_price = float(entry_saw_price.get())

    #Длина,ширина,высота детали
    x_detail = float(entry_x_detail.get())
    y_detail = float(entry_y_detail.get())
    z_detail = float(entry_z_detail.get())

    #плотность
    density = 4.5
    #Масса мерной заготовки из плиты
    mass = (x_detail*y_detail*z_detail*density)/1000000
    #Кол-во деталей в 1 тонне
    сount_details_one_tonn = 1000/mass
    #Величина врезания и величина перебега
    value_vrezaniya = 5
    value_perebega = 60
    #Кол-во полос из плиты
    count_band_plate = x_plate/(x_detail+table1["101-200"])
    #Кол-во резов с учётом резки кромок
    count_rez_with_control = count_band_plate+1
    #Тмаш1 в минутах
    T_mash1_minutes = (y_plate + value_vrezaniya+value_perebega)/10 * count_rez_with_control
    #Тмаш1 в часах
    T_mash1_hours = T_mash1_minutes/60
    #Кол-во деталей из полосы
    count_details_from_plate = math.ceil(y_plate/(y_detail+10))
    #Кол-во резов с учётом резки кромки для детали
    count_rez_with_control_detail = count_details_from_plate + 1
    #Кол-во резов для резки N кол-ва полос
    count_rez_from_plate = count_band_plate*count_rez_with_control_detail
    #Тмаш2 в минутах
    T_mash2_min = (z_detail + value_vrezaniya + value_perebega)/10 * count_rez_from_plate
    #Тмаш2 в часах
    T_mash2_hours = T_mash2_min/60
    #Кол-во деталей в 1 тонне
    count_details = count_band_plate*count_details_from_plate
    #Общая трудоёмкость резки 1 плиты на N деталей (в часах)
    summary_T_mash = T_mash1_hours+T_mash2_hours
    #Трудоёмкость резки 1 детали
    T_mash_one_detail = summary_T_mash/count_details/60
    #Тосн.1дет 1.2 - const
    T_osn_one_detail = T_mash_one_detail*1.2/60
    #Трудоёмкость резки 1 тонны
    T_mash_detail = T_mash_one_detail * count_details/60
    #Тосн.1тонны 1.2 - const
    T_osn_detail = T_mash_detail *1.2/60
    
    #Расчёт затрат на иструмент
    #Стойкость пилы (const) м^2
    plate_stamina = 8.0
    #Общая площадь реза 1 плиты
    S1 = (z_plate*(y_plate*count_rez_with_control+x_detail*count_rez_from_plate))/1000000
    #Общая площадь реза 1 тонны мерных деталей
    S2 = (S1 * сount_details_one_tonn)/count_details
    #Кол-во пил на резку 1 тонны деталей
    N = S2/plate_stamina
    #Затраты на режущий инструмент
    С = N*saw_price
    #Затраты на электричество 1 тонны 0.2 - const 7.5 - const 1.1 - const 
    Q = 0.2 * 7.5 * 1.1 * T_mash_detail
    
    CalculationData = [mass,сount_details_one_tonn,count_band_plate,count_rez_with_control,T_mash1_minutes,T_mash1_hours,count_details_from_plate,count_rez_with_control_detail,count_rez_from_plate,T_mash2_min,T_mash2_hours,count_details,summary_T_mash,T_mash_one_detail,T_osn_one_detail,T_mash_detail,T_osn_detail,S1,S2,N,С,Q]
    CalculationDataNames = ["Масса мерной заготовки из плиты","Кол-во деталей в одной тонне","Кол-во полос из плиты","Кол-во резов с учётом резки кромки","Тмаш1(мин)","Тмаш1(час)","Кол-во деталей из полосы","Кол-во резов с учётом резки кромки для детали","Кол-во резов для резки N кол-ва полос","Тмаш2(мин)","Тмаш2(час)","Кол-во деталей в 1 тонне","Общая трудоёмкость резки 1 плиты на N деталей (в часах)","Трудоёмкость резки 1 детали","Тосн.1дет","Трудоёмкость резки 1 тонны", "Тосн.1тонны", "Общая площадь реза 1 плиты", "Общая площадь реза 1 тонны мерных деталей", "Кол-во пил на резку 1 тонны деталей", "Затраты на режущий инструмент", "Затраты на электричество для 1 тонны"]
    label_calculate = ttk.Label()
    label_calculate.grid(row = 0,column=3)
    
    k = 0
    for i in CalculationData:
        label_view = ttk.Label()
        item = f"{i:.3f}"
        label_view["text"] = str(item)
        label_view.grid(row=k,column=5,sticky="w")
        k+=1
    k = 0
    for j in CalculationDataNames:
        label_view_Names = ttk.Label()
        label_view_Names["text"] = j+"="
        label_view_Names.grid(row=k,column=4,sticky="w")
        k+=1
    root.geometry("1080x480")

show_button = ttk.Button(text="Calculate", command=show)
show_button.grid(row = 1,column=2)



root.mainloop()