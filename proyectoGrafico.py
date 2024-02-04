import tkinter as tk
from dfc import arrDfc, dfc, getEbitda
from tkinter import ttk
from PIL import ImageTk, Image

ventana = tk.Tk()

ventana.title("Mi primera ventana")
ventana.geometry("600x400")
ventana.minsize(1500, 700)
ventana.configure(background="white")

frame2 = tk.Frame(ventana, width=500, height=100, bg="white")
frame2.pack()

frame = tk.Frame(ventana, width=700, height=300, bg="blue")
frame.pack()


title = tk.Label(frame2, text="Calculadora de DFC", font=("Arial", 20), bg="white")
title.pack()



addRange = 1
entries = []  # Lista para almacenar las referencias a los Entry

def calculate():
  # resultG = g.get()
  # resultRF = rf.get()
  # resultRM = rm.get()
  # print(float(resultG), float(resultRF), float(resultRM))
  
  frame3 = tk.Frame(ventana, width=500, height=100, bg="white")
  frame3.pack()
  for i in range(0, len(entries)):
    ventana.geometry("600x" + str(500+(i)*40))
    label = tk.Label(frame3, text="El valor intrinseco de " + str(entries[i].get()) + ": " + dfc(entries[i].get(), float(g.get()), float(rf.get()), float(rm.get())) , bg="gray90")
    label.pack()
    label.config(font=("Arial", 20), height=2, width=30)
    
  # dfc(ticker.get(), float(g.get()), float(rf.get()), float(rm.get()))
  
  

def createTable():
  # limpiamos la tabla
  for widget in tableFrame.winfo_children():
    widget.destroy()
  
  entry_values = [entry.get() for entry in entries]
  data = arrDfc(entry_values, float(g.get()), float(rf.get()), float(rm.get()), ebitda.get(), earnings.get(), roe.get())
  print(data)
  height = entries.__len__()
  if (ebitda.get() == 1 and earnings.get() == 1 and roe.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), show="headings", height=height)
  elif (ebitda.get() == 1 and earnings.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14), show="headings", height=height)
  elif (ebitda.get() == 1 and roe.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14), show="headings", height=height)
  elif (earnings.get() == 1 and roe.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14), show="headings", height=height)
  elif (ebitda.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13), show="headings", height=height)
  elif (earnings.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13), show="headings", height=height)
  elif (roe.get() == 1):
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13), show="headings", height=height)
  else:
    table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12), show="headings", height=height)
  
  
  # Ajustar el ancho de cada columna
  table.column(1, width=110, anchor=tk.CENTER)
  table.column(2, width=110, anchor=tk.CENTER)
  table.column(3, width=110, anchor=tk.CENTER)
  table.column(4, width=110, anchor=tk.CENTER)
  table.column(5, width=110, anchor=tk.CENTER)
  table.column(6, width=110, anchor=tk.CENTER)
  table.column(7, width=110, anchor=tk.CENTER)
  table.column(8, width=110, anchor=tk.CENTER)
  table.column(9, width=110, anchor=tk.CENTER)
  table.column(10, width=110, anchor=tk.CENTER)
  table.column(11, width=110, anchor=tk.CENTER)
  table.column(12, width=110, anchor=tk.CENTER)
  

  # Si selecciono una columna, ordenar por esa columna
  for col in (1,2,3,4,5,6,7,8,9,10,11,12):
    table.heading(col, command=lambda _col=col: \
                    treeview_sort_column(table, _col, False))
  
  table.heading(1, text="Ticker")
  table.heading(2, text="WACC")
  table.heading(3, text="2023")
  table.heading(4, text="2024")
  table.heading(5, text="2025")
  table.heading(6, text="2026")
  table.heading(7, text="2027")
  table.heading(8, text="2028")
  table.heading(9, text="Valor de la empresa")
  table.heading(10, text="Precio de la acción")
  table.heading(11, text="Valor intrínseco de la acción")
  table.heading(12, text="Diferencia")
  
  print(ebitda.get(), earnings.get(), roe.get())
  
  if (ebitda.get() == 1 and earnings.get() == 1 and roe.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.column(14, width=110, anchor=tk.CENTER)
    table.column(15, width=110, anchor=tk.CENTER)
    table.heading(13, text="EBITDA")
    table.heading(14, text="Margen de beneficio bruto")
    table.heading(15, text="ROE")
  elif (ebitda.get() == 1 and earnings.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.column(14, width=110, anchor=tk.CENTER)
    table.heading(13, text="EBITDA")
    table.heading(14, text="Margen de beneficio bruto")
  elif (ebitda.get() == 1 and roe.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.column(14, width=110, anchor=tk.CENTER)
    table.heading(13, text="EBITDA")
    table.heading(14, text="ROE")
  elif (earnings.get() == 1 and roe.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.column(14, width=110, anchor=tk.CENTER)
    table.heading(13, text="Margen de beneficio bruto")
    table.heading(14, text="ROE")
  elif (ebitda.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.heading(13, text="EBITDA")
  elif (earnings.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.heading(13, text="Margen de beneficio bruto")
  elif (roe.get() == 1):
    table.column(13, width=110, anchor=tk.CENTER)
    table.heading(13, text="ROE")
  
  table.pack(fill="both", expand=True)
  for row in data:
    table.insert('', 'end', values=row)
      

# change icon


def treeview_sort_column(tv, col, reverse):


  l = [(tv.set(k, col), k) for k in tv.get_children('')]
  l.sort(reverse=reverse)

  # Rearrange items in sorted positions.
  for index, (val, k) in enumerate(l):
    tv.move(k, '', index)

  # Reverse sort next time.
  tv.heading(col, command=lambda: \
              treeview_sort_column(tv, col, not reverse))



boton1 = tk.Button(frame, text="Calcular DFC", width=20, height=2, bg="DeepSkyBlue3", fg="white")
boton1.pack()
boton1.place(x=275, y=240)
boton1.config(command=createTable)
# boton1.config(command=calculate)

status = tk.Label(ventana, text="Status: ", bd=1, relief=tk.SUNKEN, anchor=tk.W)

def isValid():
  for entry in entries:
    if (entry.get() == ""):
      status.config(text="Status: Error")
      return False
  status.config(text="Status: ")
  return True



def add():
  
  global addRange
  addRange += 1
  entry = tk.Entry(frame, width=30, bg="gray90", validatecommand=isValid, validate="focusout")
  entry.pack()
  entry.place(x=40, y=1+(addRange-1)*40)
  entries.append(entry)  # Agregar referencia del Entry a la lista
  entries[0].insert(0, "AAPL")
  if (addRange > 5):
    print(frame.winfo_height())
    frame.configure(height=frame.winfo_height()+40)
    boton1.place(x=180, y=240+(addRange-5)*40)
    ventana.geometry("600x" + str(500+(addRange-5)*40))
    
  if (addRange > 2):
    print("create")
    bottonDelete.config(state="active", bg="DeepSkyBlue3",  fg="white")
      

def delete():
  global addRange
  if (addRange > 2):
    addRange -= 1
    entries[-1].destroy()  # Destruir el último Entry
    entries.pop()  # Eliminar referencia del Entry de la lista
    if (addRange > 4):
      frame.configure(height=frame.winfo_height()-40)
      boton1.place(x=180, y=240+(addRange-5)*40)
      ventana.geometry("600x" + str(500+(addRange-5)*40))
    else:
      # frame.configure(height=frame.winfo_height()-40)
      boton1.place(x=180, y=240)
      ventana.geometry("600x400")
    if (addRange <= 2):
      print("desactive")
      bottonDelete.config(state="disabled")
      bottonDelete.config(bg="SkyBlue1",  fg="white")

# def get_entry_values():
#   for entry in entries:
#     value = entry.get()
#     print("Valor del Entry:", value)
        

bottonDelete = tk.Button(frame, text="-", width=2, height=1, bg="SkyBlue1", fg="white")
bottonDelete.pack()
bottonDelete.config(command=delete)
bottonDelete.place(x=240, y=50)
bottonDelete.config(state="disabled")


label1 = tk.Label(frame, text="Introduce el ticker de la empresa", bg="white",)
label1.pack()
label1.place(x=40, y=15)

add()


status.pack()
status.place(x=40, y=55)

bottonAdd = tk.Button(frame, text="+", width=2, height=1, bg="DeepSkyBlue3", fg="white")
bottonAdd.pack()
bottonAdd.config(command=add)
bottonAdd.place(x=240, y=15)


label2 = tk.Label(frame, text="Introduce la tasa libre de riesgo", bg="white")
label2.pack()
label2.place(x=285, y=15)

# Ponermos un valor por defecto
rf = tk.Entry(frame, width=30, bg="gray90")
rf.insert(0, 0.04)
rf.pack()
rf.place(x=285, y=40)

label3 = tk.Label(frame, text="Introduce el rendimiento\n real del mercado (S&P 500)", bg="white")
label3.pack()
label3.place(x=280, y=80)

rm = tk.Entry(frame, width=30, bg="gray90")
rm.insert(0, 0.1)
rm.pack()
rm.place(x=285, y=120)

label4 = tk.Label(frame, text="Introduce el crecimiento perpetuo", bg="white")
label4.pack()
label4.place(x=285, y=160)

g = tk.Entry(frame, width=30, bg="gray90")
g.insert(0, 0.03)
g.pack()
g.place(x=285, y=185)

ebitda = tk.IntVar()
check = tk.Checkbutton(frame, text="Mostrar EBITDA", bg="white", variable=ebitda, onvalue=1, offvalue=0)
check.pack()
check.place(x=500, y=15)

earnings = tk.IntVar()
check2 = tk.Checkbutton(frame, text="Mostrar margen de ganacias", variable=earnings, onvalue=1, bg="white")
check2.pack()
check2.place(x=500, y=55)

roe = tk.IntVar()
check3 = tk.Checkbutton(frame, text="Mostrar ROE", variable=roe, onvalue=1, bg="white")
check3.pack()
check3.place(x=500, y=95)


tableFrame = tk.Frame(ventana, width=500, height=70, bg="white")
tableFrame.pack()

buttonXLS = tk.Button(ventana, text="Exportar a Excel", width=20, height=2, bg="DeepSkyBlue3", fg="white")
buttonXLS.pack()
buttonXLS.place(x=180, y=240)
# crear una tabla



ventana.mainloop()