import threading
import tkinter as tk
from tkinter import N, filedialog, ttk
import pandas as pd
import ttkthemes
from dfc import arrDfc

data = []
addRange = 1
entries = []

ventana = tk.Tk()

ventana.title("Calculadora de DFC")
# ventana.state("zoomed")
ventana.minsize(1500, 700)

ventana.configure(background="white")

mainFrame = tk.Frame(ventana)
mainFrame.pack(fill=tk.BOTH, expand=True)

myCanvas = tk.Canvas(mainFrame, bg="white")
myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

myScrollbar = ttk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=myCanvas.yview)
myScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear el scrollbar horizontal
myScrollbarX = ttk.Scrollbar(mainFrame, orient=tk.HORIZONTAL, command=myCanvas.xview)
myScrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

myCanvas.configure(yscrollcommand=myScrollbar.set)
# Configurar el desplazamiento horizontal del Canvas
myCanvas.configure(xscrollcommand=myScrollbarX.set)


secondFrame = tk.Frame(myCanvas, bg="white")

def center_window(event=None): 
    myCanvas.update_idletasks()

    # Obtener el tamaño del canvas y del segundo frame
    canvas_width = myCanvas.winfo_width()
    frame_width = secondFrame.winfo_reqwidth()-100

    # Calcular la posición x para centrar el segundo frame
    x = max((canvas_width - frame_width) / 2, 0)  # Asegura que x sea al menos 0

    # Centrar el segundo frame dentro del canvas
    myCanvas.create_window(x, 0, window=secondFrame, anchor="nw")
    myCanvas.configure(scrollregion=myCanvas.bbox("all"))

    # Ajustar la posición y tamaño del scrollbar vertical
    myScrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    # Configurar el desplazamiento horizontal del Canvas
    myCanvas.configure(xscrollcommand=myScrollbarX.set)
    myScrollbarX.place(x=0, y=myCanvas.winfo_height(), width=myCanvas.winfo_width(), anchor="sw")

title = tk.Label(secondFrame, text="Calculadora de DFC", font=("Arial", 20), bg="white")
title.pack()

frame = tk.Frame(secondFrame, width=700, height=300, bg="white")
frame.pack()

myCanvas.bind("<Configure>", center_window)

style = ttkthemes.ThemedStyle()

exelFrame = tk.Frame(secondFrame, width=500, height=70, bg='blue')

def createTable():
  global data
  global addRange
  status.config(text="")

  for widget in tableFrame.winfo_children():
      widget.destroy()

  entry_values = [entry.get() for entry in entries]

  if entry_values.count("") > 0:
      status.config(text="Debes llenar todos los campos")
      if (addRange > 5):
        status.place(x=293, y=(220 + (addRange-5)*40))
      else:
        status.place(x=293, y=220)
      return
  
  boton1.config(state="disabled")

  data = arrDfc(entry_values, float(g.get()), float(rf.get()), float(rm.get()), ebitda.get(), earnings.get(), roe.get(), per.get())

  tickersError = []
  for i in range(len(data)):
    if data[i][1] == "Error":
      tickersError.append(data[i][0])

  height = len(entries) - (len(tickersError))
  if (height > 0):
    columns = 13 + ebitda.get() + earnings.get() + roe.get() + per.get()
    table = ttk.Treeview(tableFrame, columns=tuple(range(1, columns+1)), show="headings", height=height)

    for i in range(1, columns+1):
        table.column(i, width=110, anchor=tk.CENTER)
        table.heading(i, command=lambda _col=i: treeview_sort_column(table, _col, False))

    headings = ["Ticker", "WACC", "FCF 2023", "FCF 2024", "FCF 2025", "FCF 2026", "FCF 2027", "FCF 2028", '% FCF', "Valor de la empresa", "Precio de la acción", "Valor intrínseco", "Diferencia"]
    if ebitda.get() == 1:
        headings.append("EBITDA")
    if earnings.get() == 1:
        headings.append("Margen de beneficio bruto")
    if roe.get() == 1:
        headings.append("ROE")
    if per.get() == 1:
        headings.append("PER")

    for i, heading in enumerate(headings, start=1):
        table.heading(i, text=heading)

    table.pack(fill="both", expand=True)
    

    # creamos una gama de colores de fondo para las filas dependiendo del valor de la columna 11
    style.configure("LightRed.TTreeview", background="#ffcccc")
    style.configure("Red.TTreeview", background="#ff6666")
    style.configure("DarkRed.TTreeview", background="#b30000")
    style.configure("LightGreen.TTreeview", background="#ccffcc")
    style.configure("Green.TTreeview", background="#66ff66")
    style.configure("DarkGreen.TTreeview", background="#00b300")

    for i, row in enumerate(data):
      if row[1] != "Error":
        second_value = float(row[12].replace('%', ''))
        if second_value < 25:  
            table.insert('', 'end', values=row, tags=('DarkRed',))
        elif second_value < 50:  
            table.insert('', 'end', values=row, tags=('Red',))
        elif second_value < 100:  
            table.insert('', 'end', values=row, tags=('LightRed',))
        elif second_value > 300:  
            table.insert('', 'end', values=row, tags=('DarkGreen',))
        elif second_value > 200:  
            table.insert('', 'end', values=row, tags=('Green',))
        elif second_value > 100:  
            table.insert('', 'end', values=row, tags=('LightGreen',))
        else:
            table.insert('', 'end', values=row)

    table.tag_configure("LightRed", background="#ffcccc")
    table.tag_configure("Red", background="#ff6666")
    table.tag_configure("DarkRed", background="#b30000", foreground="white")
    table.tag_configure("LightGreen", background="#ccffcc")
    table.tag_configure("Green", background="#66ff66" )
    table.tag_configure("DarkGreen", background="#00b300", foreground="white")


    
  if (len(tickersError) > 0):
    status.config(text=f"Los siguientes tickers no se encontraron: {tickersError}")
    if (addRange > 5):
        status.place(x=240, y=(220 + (addRange-5)*40))
    else:
      # lo colocamos en el centro de la ventana
      status.place(x=((frame.winfo_width() / 2) - 50) - (40 * len(tickersError)), y=220)

  myCanvas.update_idletasks()
  center_window()

  boton1.config(state="normal")


myCanvas.bind("<Configure>", center_window)
      
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

boton1 = tk.Button(frame, text="Calcular DFC", width=20, height=2, bg="DeepSkyBlue3", fg="white")
boton1.pack()
boton1.place(x=300, y=240)
boton_agregar_excel = tk.Button(frame, text="Agregar desde Excel", width=20, height=2, bg="DeepSkyBlue3", fg="white")

def isValid():
  global addRange
  for entry in entries:
    if (entry.get() == ""):
      status.config(text="Debes llenar todos los campos")
      if (addRange > 5):
          status.place(x=293, y=(220 + (addRange-5)*40))
      else:
        status.place(x=293, y=220)

      return False
  if (rf.get() == '' or rm.get() == '' or g.get() == ''): 
    status.config(text="Debes llenar todos los campos")
    if (addRange > 5):
        status.place(x=293, y=(220 + (addRange-5)*40))
    else:
      status.place(x=293, y=220)
    return False
  status.config(text="")
  return True

def validar_input(input_text):
    if input_text.isdigit() or input_text == "":
        return True
    else:
        return False


def add(nameCompany=None):
  global addRange
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
  
  if (addRange > 5):
      status.place(x=293, y=(220 + (addRange-5)*40))
  else:
    status.place(x=293, y=220)

  
  if (addRange > 5):
    if (nameCompany == None):
      frame.configure(height=frame.winfo_height()+40)
    else:
      frame.configure(height=frame.winfo_height()+(addRange-5)*40)
      status.place(x=100, y=220+(addRange-5)*40)
    boton1.place(x=300, y=240+(addRange-5)*40)
    boton_agregar_excel.place(x=65, y=240+(addRange-5)*40)

    myCanvas.configure(scrollregion=myCanvas.bbox("all"))
    
  if (addRange > 2):
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
    else:
      boton1.place(x=300, y=240)
    if (addRange <= 2):
      bottonDelete.config(state="disabled")
      bottonDelete.config(bg="SkyBlue1",  fg="white")


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
check2 = tk.Checkbutton(frame, text="Mostrar margen de ganacias bruto", variable=earnings, onvalue=1, bg="white")
check2.pack()
check2.place(x=500, y=55)

roe = tk.IntVar()
check3 = tk.Checkbutton(frame, text="Mostrar ROE", variable=roe, onvalue=1, bg="white")
check3.pack()
check3.place(x=500, y=95)

per = tk.IntVar()
check4 = tk.Checkbutton(frame, text="Mostrar el PER", variable=per, onvalue=1, bg="white")
check4.pack()
check4.place(x=500, y=135)


tableFrame = tk.Frame(secondFrame, width=500, height=70, bg="white")
tableFrame.pack(padx=(20, 0))


exelFrame.pack()

# porgrasFrame = tk.Frame(secondFrame, width=200, height=20, bg="yellow")
# progress = ttk.Progressbar(porgrasFrame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
buttonXLS = None
def show_button():
  global buttonXLS
  buttonXLS = tk.Button(exelFrame, text="Exportar a Excel", width=20, height=2, bg="DeepSkyBlue3", fg="white")
  buttonXLS.pack()
  buttonXLS.place(x=200, y=10)
  buttonXLS.config(command=ToExcelOrCsv)


def destroy_button():
    global buttonXLS
    if buttonXLS != None:
        buttonXLS.destroy()
        buttonXLS = None

replayDFC = 0
progress = None
def threaded_createTable():
    global replayDFC
    global progress, progressFrame, data
    replayDFC += 1
    progressFrame = tk.Frame(ventana, bg="white", borderwidth=2, relief="solid")
    progressFrame.config(width=300, height=400)
    progressFrame.pack()
    progressMessage = tk.Label(progressFrame, text="Cargando...\n Espere porfavor", bg="white")
    progressMessage.pack()
    progressMessage.config(width=20, height=5)
    progress = ttk.Progressbar(progressFrame, length=200, mode='indeterminate')
    progress.pack(padx=10, pady=(0,10))
    if replayDFC > 1:
      destroy_button()
      # if len(data) > 1:
        # progressFrame.place(x=0, y=0)
    
    # ponemos el progressbar en el centro de la ventana
    progressFrame.place(x=ventana.winfo_width() / 2 - 50, y=ventana.winfo_height() / 2 - 50)
      # progress.place(x=50, y=0)
    progress.start()
    thread = threading.Thread(target=createTable)
    thread.start()
    ventana.after(100, check_thread, thread)

def check_thread(thread):
  global data
  global progress, progressFrame
  if thread.is_alive():
        ventana.after(100, check_thread, thread)
  else:
    if progress is not None:
      progress.stop()
      progress.destroy()
      progressFrame.destroy()
      progress = None
    if not data or (len(data) == 1 and data[0][1] == "Error"):
      destroy_button()
    else:
      show_button()



boton1.config(command=threaded_createTable)
def ToExcelOrCsv():
  global data
  options = []
  if (ebitda.get() == 1):
    options.append("EBITDA")
  if (earnings.get() == 1):
    options.append("Margen de ganacia bruto")
  if (roe.get() == 1):
    options.append("ROE")
  if (per.get() == 1):
    options.append("PER")
  
  df_result = pd.DataFrame(data, columns=['Ticker', 'WACC', 'FCF 2023', 'FCF 2024', 'FCF 2025', 'FCF 2026', 'FCF 2027', 'FCF 2028', '% FCN', 'Valor de la empresa', 'Precio de la acción', 'Valor intrínseco de la acción', 'Diferencia'] + options)
  
  # Crear una ventana Tkinter sin mostrarla
  root = tk.Tk()
  root.withdraw()
  
  # Mostrar el cuadro de diálogo para guardar archivo y obtener la ruta seleccionada
  file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="dfc")
  
  if file_path:  # Comprobar si se seleccionó un archivo
      df_result.to_excel(file_path, index=False)

def agregar_datos_desde_excel():
  
  for i in range(addRange):
    delete()
  
  try:
      ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")])
      if ruta_archivo:
          # Llamar a la función para procesar el archivo Excel
          procesar_datos_desde_excel(ruta_archivo)
  except Exception as e:
      print("Ocurrió un error al abrir el archivo:", e)
  myCanvas.update_idletasks()
  center_window()

def procesar_datos_desde_excel(ruta_archivo):
    global addRange, entries
    try:
        # Cargar el archivo Excel en un DataFrame de pandas
        datos_excel = pd.read_excel(ruta_archivo)
        
        # Suponiendo que los tickers están en la primera columna del Excel
        tickers = []

        # añadimos el primer elemento de la columna 0 a la lista tickers, que es el nombre de la columna junto con los datos
        tickers.append(datos_excel.columns[0])
        # añadimos el resto de los elementos de la columna 0 a la lista tickers
        for i in range(len(datos_excel[datos_excel.columns[0]])):
          tickers.append(datos_excel[datos_excel.columns[0]][i])

        if len(entries) > 1 and entries[-1] != "":
            addRange = addRange - len(entries) + 1
        else:
            addRange = 1
            entries = []
        
        # Procesar los tickers uno por uno
        for ticker in tickers:
            # Aquí puedes agregar la lógica para procesar cada ticker, como agregarlo a la interfaz
            add(ticker)
    except Exception as e:
        print(e)
        status.config(text="Ocurrió un error al procesar el archivo Excel")

# Crear un botón para agregar datos desde un archivo Excel
boton_agregar_excel.pack()
boton_agregar_excel.place(x=65, y=240)
boton_agregar_excel.config(command=agregar_datos_desde_excel)


# crear una tabla


ventana.mainloop()