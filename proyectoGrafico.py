import stat
import tkinter as tk
import time
from tkinter import N, filedialog, ttk
from turtle import st
import pandas as pd
import ttkthemes
from dfc import arrDfc, dfc

data = []
addRange = 1
entries = []

ventana = tk.Tk()

ventana.title("Mi primera ventana")
ventana.state("zoomed")
ventana.minsize(600, 400)

ventana.configure(background="white")

mainFrame = tk.Frame(ventana)
mainFrame.pack(fill=tk.BOTH, expand=True)

myCanvas = tk.Canvas(mainFrame, bg="white")
myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

myScrollbar = ttk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=myCanvas.yview)
myScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

myCanvas.configure(yscrollcommand=myScrollbar.set)
myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion = myCanvas.bbox("all")))

secondFrame = tk.Frame(myCanvas, bg="white")

def center_window(event=None): 
    myCanvas.update_idletasks()

    # Obtener el tamaño de la ventana
    window_width = myCanvas.winfo_width()

    frame_width = secondFrame.winfo_reqwidth()

    x = (window_width - frame_width) / 2

    myCanvas.create_window((x, 0), window=secondFrame, anchor="n")
    myCanvas.configure(scrollregion=myCanvas.bbox("all"))


center_window()

myCanvas.bind("<Configure>", center_window)

title = tk.Label(secondFrame, text="Calculadora de DFC", font=("Arial", 20), bg="white")
title.pack()

frame = tk.Frame(secondFrame, width=700, height=300, bg="white")
frame.pack()


def createTable():
  global data
  status.config(text="")
  for widget in tableFrame.winfo_children():
      widget.destroy()

  start_time = time.time()

  entry_values = [entry.get() for entry in entries]
  if entry_values.count("") > 0:
      status.config(text="Debes llenar todos los campos")
      status.place(x=293, y=220)
      return

  data = arrDfc(entry_values, float(g.get()), float(rf.get()), float(rm.get()), ebitda.get(), earnings.get(), roe.get())
  end_time = time.time()
  elapsed_time = end_time - start_time
  print(f"Tiempo transcurrido: {elapsed_time} segundos")

  if type(data) == str:
      status.config(text=f"{data} comprueba que los datos sean correctos")
      status.place(x=100, y=220)
      return

  height = len(entries)*2
  columns = 12 + ebitda.get() + earnings.get() + roe.get()
  table = ttk.Treeview(tableFrame, columns=tuple(range(1, columns+1)), show="headings", height=height)

  for i in range(1, columns+1):
      table.column(i, width=110, anchor=tk.CENTER)
      table.heading(i, command=lambda _col=i: treeview_sort_column(table, _col, False))

  headings = ["Ticker", "WACC", "FCF 2023", "FCF 2024", "FCF 2025", "FCF 2026", "FCF 2027", "FCF 2028", "Valor de la empresa", "Precio de la acción", "Valor intrínseco", "Diferencia"]
  if ebitda.get() == 1:
      headings.append("EBITDA")
  if earnings.get() == 1:
      headings.append("Margen de beneficio bruto")
  if roe.get() == 1:
      headings.append("ROE")

  for i, heading in enumerate(headings, start=1):
      table.heading(i, text=heading)

  table.pack(fill="both", expand=True)

  # for i, row in enumerate(data):
  #     table.insert('', 'end', values=row)
  #     table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]))
  
  style = ttkthemes.ThemedStyle()
  # creamos una gama de colores de fondo para las filas dependiendo del valor de la columna 11
  style.configure("LightRed.TTreeview", background="#ffcccc")  # Light red for values > 20
  style.configure("Red.TTreeview", background="#ff6666")  # Red for values > 25
  style.configure("DarkRed.TTreeview", background="#b30000")  # Dark red for values > 50
  style.configure("LightGreen.TTreeview", background="#ccffcc")  # Light green for values < 0
  style.configure("Green.TTreeview", background="#66ff66")  # Green for values < -5
  style.configure("DarkGreen.TTreeview", background="#00b300")  # Dark green for values < -10

  for i, row in enumerate(data):
      second_value = float(row[11].replace('%', ''))
      if second_value > 100:  # Verificar si el segundo valor es mayor que 50
          table.insert('', 'end', values=row, tags=('DarkRed',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('DarkRed',))
      elif second_value > 50:  # Verificar si el segundo valor es mayor que 25
          table.insert('', 'end', values=row, tags=('Red',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('Red',))
      elif second_value > 0:  # Verificar si el segundo valor es mayor que 20
          table.insert('', 'end', values=row, tags=('LightRed',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('LightRed',))
      elif second_value < -100:  # Verificar si el segundo valor es menor que -10
          table.insert('', 'end', values=row, tags=('DarkGreen',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('DarkGreen',))
      elif second_value < -50:  # Verificar si el segundo valor es menor que -5
          table.insert('', 'end', values=row, tags=('Green',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('Green',))
      elif second_value < 0:  # Verificar si el segundo valor es menor que 0
          table.insert('', 'end', values=row, tags=('LightGreen',))
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]), tags=('LightGreen',))
      else:
          table.insert('', 'end', values=row)
          table.insert('', i * 2 + 1, values=('', '', '') + tuple(row[-1][0:]))
      

  table.tag_configure("LightRed", background="#ffcccc")
  table.tag_configure("Red", background="#ff6666")
  table.tag_configure("DarkRed", background="#b30000", foreground="white")
  table.tag_configure("LightGreen", background="#ccffcc")
  table.tag_configure("Green", background="#66ff66" )
  table.tag_configure("DarkGreen", background="#00b300", foreground="white")
  
  if (len(data) > 0):
    buttonXLS = tk.Button(exelFrame, text="Exportar a Excel", width=20, height=2, bg="DeepSkyBlue3", fg="white")
    buttonXLS.pack()
    buttonXLS.place(x=200, y=10)
    buttonXLS.config(command=ToExcelOrCsv)
      
def treeview_sort_column(tv, col, reverse):


  l = [(tv.set(k, col), k) for k in tv.get_children('')]
  l.sort(reverse=reverse)

  # Rearrange items in sorted positions.
  for index, (val, k) in enumerate(l):
    tv.move(k, '', index)

  # Reverse sort next time.
  tv.heading(col, command=lambda: \
              treeview_sort_column(tv, col, not reverse))


status = tk.Label(frame, bd=0, relief=tk.SUNKEN, anchor=tk.W, fg="red", bg="white")

status.pack()
status.place(x=293, y=220)

# si isValid es false el boton no se activa

boton1 = tk.Button(frame, text="Calcular DFC", width=20, height=2, bg="DeepSkyBlue3", fg="white")
boton1.pack()
boton1.place(x=300, y=240)
boton1.config(command=createTable)
# boton1.config(command=calculate)

boton_agregar_excel = tk.Button(frame, text="Agregar desde Excel", width=20, height=2, bg="DeepSkyBlue3", fg="white")

def isValid():
  for entry in entries:
    if (entry.get() == ""):
      status.config(text="Debes llenar todos los campos")
      status.place(x=200, y=220)
      return False
  if (rf.get() == '' or rm.get() == '' or g.get() == ''): 
    status.config(text="Debes llenar todos los campos")
    status.place(x=200, y=220)
    return False
  status.config(text="")
  return True

def validar_input(input_text):
    if input_text.isdigit() or input_text == "":
        return True
    else:
        return False


def add(nameCompany=None):
  
  global addRange, entries
  addRange += 1
  entry = tk.Entry(frame, width=30, bg="gray90")
  entry.pack()
  entry.place(x=40, y=1+(addRange-1)*40)
  status.config(text="")
  if (nameCompany != None):

    entry.insert(0, nameCompany)
    entries.append(entry)
    
  else:
    entries.append(entry)  # Agregar referencia del Entry a la lista
  
  # entries[0].insert(0, "AAPL")
  

  
  if (addRange > 5):
    if (nameCompany == None):
      frame.configure(height=frame.winfo_height()+40)
    else:
      frame.configure(height=frame.winfo_height()+(addRange-5)*40)
    print(addRange)
    print(frame.winfo_height())
    boton1.place(x=300, y=240+(addRange-5)*40)
    boton_agregar_excel.place(x=65, y=240+(addRange-5)*40)
    status.place(x=100, y=220+(addRange-5)*40)
    myCanvas.configure(scrollregion=myCanvas.bbox("all"))
    # ventana.geometry("600x" + str(500+(addRange-5)*40))
    
  if (addRange > 2):
    # print("create")
    bottonDelete.config(state="active", bg="DeepSkyBlue3",  fg="white")
      

def delete():
  global addRange
  status.config(text="")
  if (addRange > 2):
    addRange -= 1
    entries[-1].destroy()  # Destruir el último Entry
    entries.pop()  # Eliminar referencia del Entry de la lista
    if (addRange > 4):
      frame.configure(height=frame.winfo_height()-40)
      boton1.place(x=300, y=240+(addRange-5)*40)
      boton_agregar_excel.place(x=40, y=240+(addRange-5)*40)
      status.place(x=100, y=220+(addRange-5)*40)
      myCanvas.configure(scrollregion=myCanvas.bbox("all"))
      # ventana.geometry("600x" + str(500+(addRange-5)*40))
    else:
      # frame.configure(height=frame.winfo_height()-40)
      boton1.place(x=300, y=240)
      # ventana.geometry("600x400")
    if (addRange <= 2):
      # print("desactive")
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


bottonAdd = tk.Button(frame, text="+", width=2, height=1, bg="DeepSkyBlue3", fg="white")
bottonAdd.pack()
bottonAdd.config(command=add)
bottonAdd.place(x=240, y=15)


label2 = tk.Label(frame, text="Introduce la tasa libre de riesgo", bg="white")
label2.pack()
label2.place(x=285, y=15)

validate_cmd = ventana.register(validar_input)

rf = tk.Entry(frame, width=30, bg="gray90", validate="key", validatecommand=(validate_cmd, '%P'), textvariable=tk.StringVar(ventana, "0.04"))
rf.pack()
rf.place(x=285, y=40)

label3 = tk.Label(frame, text="Introduce el rendimiento real\ndel mercado", bg="white", justify="left")
label3.pack()
label3.place(x=285, y=80)

rm = tk.Entry(frame, width=30, bg="gray90", validate="key", validatecommand=(validate_cmd, '%P'), textvariable=tk.StringVar(ventana, "0.1"))
rm.pack()
rm.place(x=285, y=120)

label4 = tk.Label(frame, text="Introduce el crecimiento perpetuo", bg="white")
label4.pack()
label4.place(x=285, y=160)

g = tk.Entry(frame, width=30, bg="gray90", validate="key", validatecommand=(validate_cmd, '%P'), textvariable=tk.StringVar(ventana, "0.03"))
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


tableFrame = tk.Frame(secondFrame, width=500, height=70, bg="white")
tableFrame.pack()

exelFrame = tk.Frame(secondFrame, width=500, height=70, bg='white')
exelFrame.pack()

def ToExcelOrCsv():
  global data
  options = []
  if (ebitda.get() == 1):
    options.append("EBITDA")
  if (earnings.get() == 1):
    options.append("Margen de beneficio bruto")
  if (roe.get() == 1):
    options.append("ROE")
  
  newLits = []
  # recorremos data y a cada fila le quitamos el último elemento y lo guardamos en una nueva lista
  for i in range(len(data)):
    # guardonel ultimo elemento de cada fila en una lista
    newLits.append(data[i][-1])
    
    # qutiando el último elemento de cada fila
    data[i] = data[i][:-1]
  
  # ayadimos debajo de cada fila de data una fila con los valores de la lista newLita
  
  # Inserto una columna en la posición 3 con el primer elemento de la lista newLits
  # data[0].insert(3, newLits[0][0])
  # data[0].insert(5, newLits[0][1])
  # data[0].insert(7, newLits[0][2])
  # data[0].insert(9, newLits[0][3])
  
  for i in range(len(data)):
    for j in range(len(newLits[i])):
      data[i].insert(4 + 2*j, newLits[i][j])
    
  
  # print(newLits)
  
  df_result = pd.DataFrame(data, columns=['Ticker', 'WACC', 'FCF 2023', 'FCF 2024', 'FCN', 'FCF 2025', 'FCN', 'FCF 2026',  'FCN','FCF 2027', 'FCN', 'FCF 2028', 'FCN', 'Valor de la empresa', 'Precio de la acción', 'Valor intrínseco de la acción', 'Diferencia'] + options)
  
  # Crear una ventana Tkinter sin mostrarla
  root = tk.Tk()
  root.withdraw()
  
  # Mostrar el cuadro de diálogo para guardar archivo y obtener la ruta seleccionada
  file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="dfc")
  
  if file_path:  # Comprobar si se seleccionó un archivo
      df_result.to_excel(file_path, index=False)
      # print(f"El archivo se guardó correctamente en: {file_path}")

def agregar_datos_desde_excel():
    try:
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")])
        if ruta_archivo:
            # Llamar a la función para procesar el archivo Excel
            procesar_datos_desde_excel(ruta_archivo)
    except Exception as e:
        print("Ocurrió un error al abrir el archivo:", e)

def procesar_datos_desde_excel(ruta_archivo):
  global addRange, entries
  try:
    # Cargar el archivo Excel en un DataFrame de pandas
    datos_excel = pd.read_excel(ruta_archivo)
    if (len(entries) > 1 and entries[-1] != ""):
      addRange = addRange - len(entries) + 1
    else:
      addRange = 1
      entries = []
    # Extraer los nombres de empresas (suponiendo que la columna se llama 'Nombre de la Empresa')
    nombres_empresas = datos_excel['Ticker'].tolist()
    
    # Hacer algo con los nombres de empresas, como agregarlos a la lista de entradas o procesarlos de alguna otra manera
    for nombre_empresa in nombres_empresas:
        # Aquí puedes agregar la lógica para procesar cada nombre de empresa, como agregarlo a la interfaz1
        print("Nombre de empresa:", nombre_empresa)
        add(nombre_empresa)
        pass
    
    print("Datos del archivo Excel procesados correctamente.")
  except Exception as e:
    print("Ocurrió un error al procesar el archivo Excel:", e)

# Crear un botón para agregar datos desde un archivo Excel
boton_agregar_excel.pack()
boton_agregar_excel.place(x=65, y=240)
boton_agregar_excel.config(command=agregar_datos_desde_excel)


# crear una tabla


ventana.mainloop()