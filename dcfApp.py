import threading
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import ttkthemes
from dcfArrayCalculator import DcfArrayCalculator


class DcfApp:
    def __init__(self, master):
        """
        Inicializa de DcfApp.

        Args:
            master: El widget principal de la aplicación.
        """
        self.master = master
        """Segundo ventana principal de la aplicación"""
        self.data = []
        """Lista que contiene los datos de la tabla de resultados."""
        self.addRange = 1
        """Número de campos de entrada para el ticker de la empresa."""
        self.entries = []
        """Lista que contiene los campos de entrada para el ticker de la empresa."""
        self.ventana = master
        """Ventana principal de la aplicación."""
        self.replayDCF = 0
        """Número de veces que se ha ejecutado el cálculo DCF."""
        self.progress = None
        """Barra de progreso para el cálculo DCF."""
        self.buttonXLS = None
        """Botón para exportar a Excel."""
        self.dataArray = []

        self.create_widgets()

    def create_widgets(self):
        """
        Crea los widgets para la interfaz de la aplicación.
        """
        self.ventana.title("Calculadora de DCF")
        self.ventana.minsize(1500, 700)
        self.ventana.configure(background="white")

        self.mainFrame = tk.Frame(self.ventana)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.myCanvas = tk.Canvas(self.mainFrame, bg="white")
        self.myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.myScrollbar = tk.ttk.Scrollbar(
            self.mainFrame, orient=tk.VERTICAL, command=self.myCanvas.yview
        )
        self.myScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.myScrollbarX = tk.ttk.Scrollbar(
            self.mainFrame, orient=tk.HORIZONTAL, command=self.myCanvas.xview
        )
        self.myScrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        self.myCanvas.configure(yscrollcommand=self.myScrollbar.set)
        self.myCanvas.configure(xscrollcommand=self.myScrollbarX.set)

        self.secondFrame = tk.Frame(self.myCanvas, bg="white")

        self.title = tk.Label(
            self.secondFrame, text="Calculadora de DCF", font=("Arial", 20), bg="white"
        )
        self.title.pack()

        self.frame = tk.Frame(self.secondFrame, width=1000, height=300, bg="white")
        self.frame.pack()

        self.myCanvas.bind("<Configure>", self.center_window)

        self.style = ttkthemes.ThemedStyle()

        

        self.status = tk.Label(
            self.frame, bd=0, relief=tk.SUNKEN, anchor=tk.W, fg="red", bg="white"
        )
        self.status.pack()

        self.boton1 = tk.Button(
            self.frame,
            text="Calcular DCF",
            width=20,
            height=2,
            bg="DeepSkyBlue3",
            fg="white",
        )
        self.boton1.pack()
        self.boton1.place(x=300, y=240)
        self.boton_agregar_excel = tk.Button(
            self.frame,
            text="Agregar desde Excel",
            width=20,
            height=2,
            bg="DeepSkyBlue3",
            fg="white",
        )

        self.bottonDelete = tk.Button(
            self.frame, text="-", width=2, height=1, bg="SkyBlue1", fg="white"
        )
        self.bottonDelete.pack()
        self.bottonDelete.config(command=self.delete)
        self.bottonDelete.place(x=240, y=50)
        self.bottonDelete.config(state="disabled")

        self.label1 = tk.Label(
            self.frame, text="Introduce el ticker de la empresa", bg="white"
        )
        self.label1.pack()
        self.label1.place(x=40, y=15)

        tickerMessage = "El ticker de la empresa es el símbolo que se utiliza para identificar una empresa en el mercado de valores, \ncomo AAPL para Apple Inc. o MSFT para Microsoft Corporation."
        self.label1.bind(
            "<Enter>", lambda event: self.enter(event, tickerMessage, self.label1)
        )
        self.label1.bind("<Leave>", self.leave)

        self.add()

        self.bottonAdd = tk.Button(
            self.frame, text="+", width=2, height=1, bg="DeepSkyBlue3", fg="white"
        )
        self.bottonAdd.pack()
        self.bottonAdd.config(command=self.add)
        self.bottonAdd.place(x=240, y=15)

        self.label2 = tk.Label(
            self.frame, text="Introduce la tasa libre de riesgo", bg="white"
        )
        self.label2.pack()
        self.label2.place(x=285, y=15)

        self.rfMessage = "La tasa libre de riesgo es el rendimiento que se espera de una inversión libre de riesgo, \ncomo los bonos del Tesoro de EE. UU. a 10 años (4%)"
        self.label2.bind(
            "<Enter>", lambda event: self.enter(event, self.rfMessage, self.label2)
        )
        self.label2.bind("<Leave>", self.leave)

        self.validate_cmd = self.ventana.register(self.validar_input)

        self.rf = tk.Entry(
            self.frame,
            width=30,
            bg="gray90",
            validate="key",
            validatecommand=(self.validate_cmd, "%P"),
            textvariable=tk.StringVar(self.ventana, "0.04"),
        )
        self.rf.pack()
        self.rf.place(x=285, y=40)

        self.label3 = tk.Label(
            self.frame,
            text="Introduce el rendimiento real\ndel mercado",
            bg="white",
            justify="left",
        )
        self.label3.pack()
        self.label3.place(x=285, y=80)

        self.rmMessage = "El rendimiento real del mercado es el rendimiento que se espera de una inversión en el mercado de valores, \ncomo el S&P 500 (10%)"
        self.label3.bind(
            "<Enter>", lambda event: self.enter(event, self.rmMessage, self.label3)
        )
        self.label3.bind("<Leave>", self.leave)

        self.rm = tk.Entry(
            self.frame,
            width=30,
            bg="gray90",
            validate="key",
            validatecommand=(self.validate_cmd, "%P"),
            textvariable=tk.StringVar(self.ventana, "0.1"),
        )
        self.rm.pack()
        self.rm.place(x=285, y=120)

        self.label4 = tk.Label(
            self.frame, text="Introduce el crecimiento perpetuo", bg="white"
        )
        self.label4.pack()
        self.label4.place(x=285, y=160)

        self.gMessage = "El crecimiento perpetuo es el crecimiento constante que se espera de una empresa a largo plazo, \ncomo el crecimiento del PIB (3%)"
        self.label4.bind(
            "<Enter>", lambda event: self.enter(event, self.gMessage, self.label4)
        )
        self.label4.bind("<Leave>", self.leave)

        self.g = tk.Entry(
            self.frame,
            width=30,
            bg="gray90",
            validate="key",
            validatecommand=(self.validate_cmd, "%P"),
            textvariable=tk.StringVar(self.ventana, "0.03"),
        )
        self.g.pack()
        self.g.place(x=285, y=185)

        self.ebitda = tk.IntVar()
        self.check = tk.Checkbutton(
            self.frame,
            text="Mostrar EBITDA",
            bg="white",
            variable=self.ebitda,
            onvalue=1,
            offvalue=0,
        )
        self.check.pack()
        self.check.place(x=500, y=15)

        self.ebitdaMessage = "El EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization) es una medida de la rentabilidad de una empresa, \nantes de intereses, impuestos, depreciación y amortización."
        self.check.bind(
            "<Enter>", lambda event: self.enter(event, self.ebitdaMessage, self.check)
        )
        self.check.bind("<Leave>", self.leave)

        self.earnings = tk.IntVar()
        self.check2 = tk.Checkbutton(
            self.frame,
            text="Mostrar margen de ganacias bruto",
            variable=self.earnings,
            onvalue=1,
            bg="white",
        )
        self.check2.pack()
        self.check2.place(x=500, y=55)

        self.earningsMessage = "El margen de ganancias bruto es la relación entre las ganancias brutas y los ingresos totales. \nUn margen de ganancias bruto más alto puede indicar que la empresa es más eficiente."
        self.check2.bind(
            "<Enter>",
            lambda event: self.enter(event, self.earningsMessage, self.check2),
        )
        self.check2.bind("<Leave>", self.leave)

        self.roe = tk.IntVar()
        self.check3 = tk.Checkbutton(
            self.frame, text="Mostrar ROE", variable=self.roe, onvalue=1, bg="white"
        )
        self.check3.pack()
        self.check3.place(x=500, y=95)

        self.roeMessage = "El ROE (Return on Equity) es la relación entre las ganancias netas y el patrimonio neto de la empresa. \nUn ROE más alto puede indicar que la empresa es más eficiente."
        self.check3.bind(
            "<Enter>", lambda event: self.enter(event, self.roeMessage, self.check3)
        )
        self.check3.bind("<Leave>", self.leave)

        self.per = tk.IntVar()
        self.check4 = tk.Checkbutton(
            self.frame, text="Mostrar el PER", variable=self.per, onvalue=1, bg="white"
        )
        self.check4.pack()
        self.check4.place(x=500, y=135)

        self.perMessage = (
            "El PER (Price Earnings Ratio) es la relación entre el precio de una acción y \n"
            "las ganancias por acción de la empresa. Un PER más alto puede indicar \n"
            "que la acción está sobrevalorada, mientras que un PER más bajo puede \n"
            "indicar que la acción está infravalorada.\n"
            " - PER bajo: 0-10\n"
            " - PER medio: 10-20\n"
            " - PER alto: +20"
        )
        self.check4.bind(
            "<Enter>", lambda event: self.enter(event, self.perMessage, self.check4)
        )
        self.check4.bind("<Leave>", self.leave)

        self.seeking = tk.IntVar()
        self.check5 = tk.Checkbutton(
            self.frame,
            text="Calcular con el crecimiento de Seeking Alpha",
            variable=self.seeking,
            onvalue=1,
            bg="white",
        )
        self.check5.pack()
        self.check5.place(x=500, y=175)

        self.seekingMessage = (
            "El crecimiento de Seeking Alpha es el crecimiento que se espera de una empresa a largo plazo, \n"
            "según el consenso de analistas de Seeking Alpha."
        )
        self.check5.bind(
            "<Enter>", lambda event: self.enter(event, self.seekingMessage, self.check5)
        )
        self.check5.bind("<Leave>", self.leave)

        self.zacks = tk.IntVar()
        self.check6 = tk.Checkbutton(
            self.frame,
            text="Calcular con el crecimiento de Zacks",
            variable=self.zacks,
            onvalue=1,
            bg="white",
        )
        self.check6.pack()
        self.check6.place(x=710, y=15)

        self.zacksMessage = (
            "El crecimiento de Zacks es el crecimiento que se espera de una empresa a largo plazo, \n"
            "según el consenso de analistas de Zacks."
        )
        self.check6.bind(
            "<Enter>", lambda event: self.enter(event, self.zacksMessage, self.check6)
        )
        self.check6.bind("<Leave>", self.leave)

        self.tableFrame = tk.Frame(self.secondFrame, width=500, height=70, bg="white")
        self.tableFrame.pack(padx=(20, 0))

        self.tableFrame2 = tk.Frame(self.secondFrame, width=500, height=70, bg="white")
        self.tableFrame2.pack(padx=(20, 0), pady=(20, 0))

        self.tableFrame3 = tk.Frame(self.secondFrame, width=500, height=70, bg="white")
        self.tableFrame3.pack(padx=(20, 0), pady=(20, 0))

        self.exelFrame = tk.Frame(self.frame, width=200, height=50, bg="blue")
        self.exelFrame.pack()
        self.exelFrame.place(x=530, y=240)

        self.boton1.config(command=self.threaded_create_table)

        self.boton_agregar_excel.pack()
        self.boton_agregar_excel.place(x=65, y=240)
        self.boton_agregar_excel.config(command=self.agregar_datos_desde_excel)

    def center_window(self, event=None):
        """
        Centra la ventana secundaria en el lienzo cuando se redimensiona.

        Args:
            event: El evento que activa la función (opcional).
        """
        self.myCanvas.update_idletasks()

        canvas_width = self.myCanvas.winfo_width()
        frame_width = self.secondFrame.winfo_reqwidth()
        x = max((canvas_width - frame_width) / 2, 0)

        self.myCanvas.create_window(x, 0, window=self.secondFrame, anchor="nw")
        self.myCanvas.configure(scrollregion=self.myCanvas.bbox("all"))

        self.myScrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.myCanvas.configure(xscrollcommand=self.myScrollbarX.set)
        self.myScrollbarX.place(
            x=0,
            y=self.myCanvas.winfo_height(),
            width=self.myCanvas.winfo_width(),
            anchor="sw",
        )

    def validar_input(self, P):
        """
        Valida la entrada del usuario para asegurar que sea un número.

        Args:
            P: El valor a validar.

        Returns:
            True si la entrada es válida, False en caso contrario.
        """
        if P == "" or P.isdigit():
            return True
        try:
            float(P)
        except ValueError:
            return False
        return True

    def add(self, nameCompany=None):
        """
        Agrega un campo de entrada para el ticker de la empresa.

        Args:
            nameCompany (str): El nombre de la empresa (opcional).
        """
        self.addRange += 1
        self.entry = tk.Entry(self.frame, width=30, bg="gray90")
        self.entry.pack()
        self.entry.place(x=40, y=1 + (self.addRange - 1) * 40)
        self.status.config(text="")

        if nameCompany is not None:
            self.entry.insert(0, nameCompany)
        self.entries.append(self.entry)

        if self.addRange > 5:
            self.frame.configure(
                height=self.frame.winfo_height()
                + (40 if nameCompany is None else (self.addRange - 5) * 40)
            )
            self.status.place(x=100, y=220 + (self.addRange - 5) * 40)
            self.boton1.place(x=300, y=240 + (self.addRange - 5) * 40)
            self.exelFrame.place(x=530, y=240 + (self.addRange - 5) * 40)
            self.boton_agregar_excel.place(x=65, y=240 + (self.addRange - 5) * 40)
            self.myCanvas.configure(scrollregion=self.myCanvas.bbox("all"))
        else:
            self.status.place(x=293, y=220)

        if self.addRange > 2:
            self.bottonDelete.config(state="active", bg="DeepSkyBlue3", fg="white")

    def delete(self):
        """
        Elimina el último campo de entrada para el ticker de la empresa.
        """
        self.status.config(text="")
        if self.addRange > 2:
            self.addRange -= 1
            self.entries[-1].destroy()  # Destruir el último Entry
            self.entries.pop()  # Eliminar referencia del Entry de la lista
            if self.addRange > 4:
                self.frame.configure(height=self.frame.winfo_height() - 40)
                self.boton1.place(x=300, y=240 + (self.addRange - 5) * 40)
                self.boton_agregar_excel.place(x=40, y=240 + (self.addRange - 5) * 40)
                self.status.place(x=100, y=220 + (self.addRange - 5) * 40)
                self.myCanvas.configure(scrollregion=self.myCanvas.bbox("all"))
            else:
                self.boton1.place(x=300, y=240)
            if self.addRange <= 2:
                self.bottonDelete.config(state="disabled")
                self.bottonDelete.config(bg="SkyBlue1", fg="white")

    def destroy_button(self):
        """
        Destruye el botón de archivo Excel si existe.
        """
        if self.buttonXLS:
            self.buttonXLS.destroy()
            self.buttonXLS = None

    def show_button(self):
        """
        Muestra el botón para exportar a Excel.
        """
        self.buttonXLS = tk.Button(
            self.exelFrame,
            text="Exportar a Excel",
            width=20,
            height=2,
            bg="DeepSkyBlue3",
            fg="white",
        )
        self.buttonXLS.pack()
        self.buttonXLS.place(x=0, y=0)
        self.buttonXLS.config(command=self.to_excel_or_csv_arr)

    def create_tables(self):
        """
        Crea las tablas con los resultados del cálculo DCF para cada opción de crecimiento.
        """
        self.dataArray.clear()

        frames = [self.tableFrame, self.tableFrame2, self.tableFrame3]
        growthOptions = ["yahoo"]

        framesOpt = [self.tableFrame, self.tableFrame2, self.tableFrame3]
        for frameOpt in framesOpt:
            for widget in frameOpt.winfo_children():
                widget.destroy()

        if self.seeking.get():
            growthOptions.append("seeking")

        if self.zacks.get():
            growthOptions.append("zacks")

        for i, option in enumerate(growthOptions):
            self.create_table(option, frames[i])
        
        growthOptions.clear()

    def create_table(self, growthOption, frame):
        """
        Crea una tabla con los resultados del cálculo DCF.
        """
        # for widget in frame.winfo_children():
        #     widget.destroy()

        menssageOption = ""
        if growthOption == "yahoo":
            menssageOption = "Crecimiento de Yahoo Finance"
        elif growthOption == "seeking":
            menssageOption = "Crecimiento de Seeking Alpha"
        elif growthOption == "zacks":
            menssageOption = "Crecimiento de Zacks"

        labelOptions = tk.Label(
            frame, text=menssageOption, font=("Arial", 8), bg="white", justify="left"
        )
        labelOptions.pack()

        entry_values = [entry.get() for entry in self.entries]

        if entry_values.count("") > 0:
            self.status.config(text="Debes llenar todos los campos")
            if self.addRange > 5:
                self.status.place(x=293, y=(220 + (self.addRange - 5) * 40))
            else:
                self.status.place(x=293, y=220)
            return

        if self.rf.get() == "" or self.rm.get() == "" or self.g.get() == "":
            self.status.config(text="Debes llenar todos los campos")
            if self.addRange > 5:
                self.status.place(x=293, y=(220 + (self.addRange - 5) * 40))
            else:
                self.status.place(x=293, y=220)
            return

        self.boton1.config(state="disabled")
        dataDcfResult = DcfArrayCalculator()
        self.data = dataDcfResult.arrDcf(
            entry_values,
            float(self.g.get()),
            float(self.rf.get()),
            float(self.rm.get()),
            self.ebitda.get(),
            self.earnings.get(),
            self.roe.get(),
            self.per.get(),
            growthOption,
        )
        self.dataArray.append(self.data)
        tickersError = []
        for i in range(len(self.data)):
            if self.data[i][1] == "Error":
                tickersError.append(self.data[i][0])

        height = len(self.entries) - (len(tickersError))
        if height > 0:
            columns = (
                13
                + self.ebitda.get()
                + self.earnings.get()
                + self.roe.get()
                + self.per.get()
            )
            table = tk.ttk.Treeview(
                frame,
                columns=tuple(range(1, columns + 1)),
                show="headings",
                height=height,
            )

            for i in range(1, columns + 1):
                table.column(i, width=110, anchor=tk.CENTER)
                table.heading(
                    i,
                    command=lambda _col=i: self.treeview_sort_column(
                        table, _col, False
                    ),
                )

            headings = [
                "Ticker",
                "WACC",
                "FCF 2023",
                "FCF 2024",
                "FCF 2025",
                "FCF 2026",
                "FCF 2027",
                "FCF 2028",
                "% FCF",
                "Valor de la empresa",
                "Precio de la acción",
                "Valor intrínseco",
                "Diferencia",
            ]
            if self.ebitda.get() == 1:
                headings.append("EBITDA")
            if self.earnings.get() == 1:
                headings.append("Margen de beneficio bruto")
            if self.roe.get() == 1:
                headings.append("ROE")
            if self.per.get() == 1:
                headings.append("PER")

            for i, heading in enumerate(headings, start=1):
                table.heading(i, text=heading)

            table.pack(fill="both", expand=True)

            self.style.configure("LightRed.TTreeview", background="#ffcccc")
            self.style.configure("Red.TTreeview", background="#ff6666")
            self.style.configure("DarkRed.TTreeview", background="#b30000")
            self.style.configure("LightGreen.TTreeview", background="#ccffcc")
            self.style.configure("Green.TTreeview", background="#66ff66")
            self.style.configure("DarkGreen.TTreeview", background="#00b300")

            for i, row in enumerate(self.data):
                if row[1] != "Error":
                    second_value = float(row[12].replace("%", ""))
                    if second_value < 25:
                        table.insert("", "end", values=row, tags=("DarkRed",))
                    elif second_value < 50:
                        table.insert("", "end", values=row, tags=("Red",))
                    elif second_value < 100:
                        table.insert("", "end", values=row, tags=("LightRed",))
                    elif second_value > 300:
                        table.insert("", "end", values=row, tags=("DarkGreen",))
                    elif second_value > 200:
                        table.insert("", "end", values=row, tags=("Green",))
                    elif second_value > 100:
                        table.insert("", "end", values=row, tags=("LightGreen",))
                    else:
                        table.insert("", "end", values=row)

            table.tag_configure("LightRed", background="#ffcccc")
            table.tag_configure("Red", background="#ff6666")
            table.tag_configure("DarkRed", background="#b30000", foreground="white")
            table.tag_configure("LightGreen", background="#ccffcc")
            table.tag_configure("Green", background="#66ff66")
            table.tag_configure("DarkGreen", background="#00b300", foreground="white")

        if len(tickersError) > 0:
            self.status.config(
                text=f"Los siguientes tickers no se encontraron: {tickersError}"
            )
            if self.addRange > 5:
                self.status.place(x=240, y=(220 + (self.addRange - 5) * 40))
            else:
                self.status.place(
                    x=((self.frame.winfo_width() / 2) - 50) - (40 * len(tickersError)),
                    y=220,
                )

        self.myCanvas.update_idletasks()
        self.center_window()

        self.boton1.config(state="normal")

    def treeview_sort_column(self, tv, col, reverse):
        """
        Ordena las columnas de la tabla.
        Args:
            tv (ttk.Treeview): El widget Treeview.
            col (int): El índice de la columna a ordenar.
            reverse (bool): True para orden descendente, False para orden ascendente.
        """
        l = [(tv.set(k, col), k) for k in tv.get_children("")]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, "", index)

        # Reverse sort next time.
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def enter(self, event, message, label):
        """
        Muestra un tooltip cuando el cursor entra en el área del widget.

        Args:
            event: El evento de entrada que desencadenó la función.
            message (str): El mensaje a mostrar en el tooltip.
            label: El widget Label asociado al tooltip.
        """
        x, y, _, _ = self.check4.bbox("insert")
        x += label.winfo_rootx() + 25
        y += label.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.check4)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip,
            text=message,
            bg="white",
            relief="solid",
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()

    def leave(self, event):
        """
        Oculta el tooltip cuando el cursor sale del área del widget.
        """
        if self.tooltip:
            self.tooltip.destroy()

    def threaded_create_table(self):
        """
        Inicia un hilo para crear la tabla de resultados de DCF.
        """
        self.replayDCF += 1
        self.progressFrame = tk.Frame(
            self.ventana, bg="white", borderwidth=2, relief="solid"
        )
        self.progressFrame.config(width=300, height=400)
        self.progressFrame.pack()
        self.progressMessage = tk.Label(
            self.progressFrame, text="Cargando...\n Espere por favor", bg="white"
        )
        self.progressMessage.pack()
        self.progressMessage.config(width=20, height=5)
        self.progress = tk.ttk.Progressbar(
            self.progressFrame, length=200, mode="indeterminate"
        )
        self.progress.pack(padx=10, pady=(0, 10))
        if self.replayDCF > 1:
            self.destroy_button()

        self.progressFrame.place(
            x=self.ventana.winfo_width() / 2 - 50,
            y=self.ventana.winfo_height() / 2 - 50,
        )
        self.progress.start()
        thread = threading.Thread(target=self.create_tables)
        thread.start()
        self.ventana.after(100, self.check_thread, thread)

    def check_thread(self, thread):
        """
        Verifica periódicamente si el hilo de creación de tabla está vivo.
        """
        if thread.is_alive():
            self.ventana.after(100, self.check_thread, thread)
        else:
            if self.progress is not None:
                self.progress.stop()
                self.progress.destroy()
                self.progressFrame.destroy()
                progress = None
            if not self.data or (len(self.data) == 1 and self.data[0][1] == "Error"):
                self.destroy_button()
            else:
                self.show_button()

    def to_excel_or_csv_arr(self):
        for i in range(len(self.dataArray)):
            self.data = self.dataArray[i]
            self.to_excel_or_csv()

    def to_excel_or_csv(self):
        """Función para exportar los datos a un archivo Excel o CSV"""
        options = []
        if self.ebitda.get() == 1:
            options.append("EBITDA")
        if self.earnings.get() == 1:
            options.append("Margen de ganacia bruto")
        if self.roe.get() == 1:
            options.append("ROE")
        if self.per.get() == 1:
            options.append("PER")

        df_result = pd.DataFrame(
            self.data,
            columns=[
                "Ticker",
                "WACC",
                "FCF 2023",
                "FCF 2024",
                "FCF 2025",
                "FCF 2026",
                "FCF 2027",
                "FCF 2028",
                "% FCN",
                "Valor de la empresa",
                "Precio de la acción",
                "Valor intrínseco de la acción",
                "Diferencia",
            ]
            + options,
        )

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="dcf",
        )

        if file_path:
            df_result.to_excel(file_path, index=False)

    def agregar_datos_desde_excel(self):
        """
        Agrega tickers desde un archivo de Excel al formulario.
        """
        for i in range(self.addRange):
            self.delete()

        try:
            ruta_archivo = filedialog.askopenfilename(
                filetypes=[
                    ("Archivos de Excel", "*.xlsx"),
                    ("Todos los archivos", "*.*"),
                ]
            )
            if ruta_archivo:
                self.procesar_datos_desde_excel(ruta_archivo)
        except Exception as e:
            print("Ocurrió un error al abrir el archivo:", e)
        self.myCanvas.update_idletasks()
        self.center_window()

    def procesar_datos_desde_excel(self, ruta_archivo):
        """
        Procesa los datos desde un archivo de Excel y los agrega al formulario.

        Parameters:
            ruta_archivo (str): La ruta del archivo de Excel.
        """
        try:
            self.datos_excel = pd.read_excel(ruta_archivo)
            self.tickers = []
            self.tickers.append(self.datos_excel.columns[0])

            for i in range(len(self.datos_excel[self.datos_excel.columns[0]])):
                self.tickers.append(self.datos_excel[self.datos_excel.columns[0]][i])

            if len(self.entries) > 1 and self.entries[-1] != "":
                self.addRange = self.addRange - len(self.entries) + 1
            else:
                self.addRange = 1
                self.entries = []

            for ticker in self.tickers:
                self.add(ticker)
        except Exception as e:
            print(e)
            self.status.config(text="Ocurrió un error al procesar el archivo Excel")


def main():
    """
    Función principal para iniciar la aplicación.
    """
    root = tk.Tk()
    app = DcfApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
