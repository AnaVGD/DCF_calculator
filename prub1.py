import yfinance as yf
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup

# import matplotlib.pyplot as plt

# Creación del objeto de Ticker para el símbolo específico de una acción

ticker = yf.Ticker("GOOG")


# Obtenemos el valor de la deuda total (total debt) del ultimo año de yahoo finance
d = ticker.balance_sheet.loc['Total Debt']
i = 0
last_year_total_debt = d.iloc[i]
while math.isnan(d.iloc[i]):
  i += 1
  last_year_total_debt = d.iloc[i]
print('Valor de la deuda total: ', last_year_total_debt)

#### Calcular WACC ####

# Calculo de los fondos propios
def waccCalculator():
  
  # 1. Obtenemos la tasa libre de riesgo (rf) Tasa de un Bono del Tesoro de 5 años
  rf = 0.04243

  # 2. Obtenemos el riesgo sistemático (beta) de la acción de yahoo finance
  beta = ticker.info['beta']
  print('Beta: ', beta)

  # 3. Indicamos el rendimiento real del mercado (rm) en este caso el S&P 500
  rm = 0.1

  # 4. Calculamos el costo del capital de los fondos propios (ke)
  ke = rf + (beta * (rm - rf))
  print('Costo del capital de los fondos propios: ', ke)

  # 6. Obtenemos la capitalización bursátil (market cap) del ultimo año de yahoo finance
  e = ticker.info['marketCap']
  print('Capitalización bursátil: ', e)

  # 7. Calculamos la deuda total (E + D)
  total_debt_ED = e + last_year_total_debt
  print('Deuda total: ', total_debt_ED)

  # 8. Calculamos el total de los fondos propios (ke * (E / (E + D)))
  total_equity = ke * (e / total_debt_ED)
  print('Total de los fondos propios: ', format((total_equity * 100), '.2f'), '%')
  # print('')

  # Calculo del coste de la deuda
  # 1. Obtenemos el gasto por interese (Interest Expense) del ultimo año de yahoo finance
  interest_expense = ticker.financials.loc['Interest Expense']
  i = 0
  last_year_interest_expense = interest_expense.iloc[i]
  while math.isnan(interest_expense.iloc[i]):
    i += 1
    last_year_interest_expense = interest_expense.iloc[i]

  print('Gasto por intereses: ', last_year_interest_expense)

  # 2. obtener la deuda a corto plazo (current debt) del ultimo año de yahoo finance
  current_debt = ticker.balance_sheet.loc['Current Debt And Capital Lease Obligation']
  # print(current_debt)
  i = 0
  last_year_current_debt = current_debt.iloc[i]
  while math.isnan(current_debt.iloc[i]):
    i += 1
    last_year_current_debt = current_debt.iloc[i]

  print('Deuda a corto plazo: ', last_year_current_debt)

  # 3. obtener la deuda a largo plazo (long term debt) del ultimo año de yahoo finance
  long_term_debt = ticker.balance_sheet.loc['Long Term Debt']
  i = 0
  last_year_long_term_debt = long_term_debt.iloc[i]
  while math.isnan(long_term_debt.iloc[i]):
    i += 1
    last_year_long_term_debt = long_term_debt.iloc[i]

  print('Deuda a largo plazo: ', last_year_long_term_debt)

  # 4. Obtener el coste de la deuda financiera (kd)
  kd = (last_year_interest_expense / (last_year_current_debt + last_year_long_term_debt))
  print('Coste de la deuda financiera: ', format((kd * 100), '.2f'), '%')

  # 5. Obtener el ingreso por gastos de impuestos (tax Provision) del ultimo año de yahoo finance
  tax_provision = ticker.income_stmt.loc['Tax Provision']
  i = 0
  last_year_tax_provision = tax_provision.iloc[i]
  while math.isnan(tax_provision.iloc[i]):
    i += 1
    last_year_tax_provision = tax_provision.iloc[i]

  print('Ingreso por gastos de impuestos: ', last_year_tax_provision)

  # 6. Obtener el ingreso antes de impuestos (Pretax Income) del ultimo año de yahoo finance
  pretax_income = ticker.income_stmt.loc['Pretax Income']
  i = 0
  last_year_pretax_income = pretax_income.iloc[i]
  while math.isnan(pretax_income.iloc[i]):
    i += 1
    last_year_pretax_income = pretax_income.iloc[i]

  print('Ingreso antes de impuestos: ', last_year_pretax_income)

  # 7. Calculo la tasa impositiva (T)
  t = last_year_tax_provision / last_year_pretax_income
  print('Tasa impositiva: ', format((t * 100), '.2f'), '%')

  # 8. Calculo el coste de la deuda
  total_debt_cost = kd * (1 - t) * ( last_year_total_debt / total_debt_ED)
  print('Coste de la deuda: ', format((total_debt_cost * 100), '.2f'), '%')

  #### Calculo del WACC ####
  # 1. Calculo el WACC
  wacc = total_equity + total_debt_cost
  print('\nWACC: ', format((wacc * 100), '.2f'), '%')
  return wacc

# waccCalculator()

#### Calculo el DFC ####
def growthEstimates():

  # Definir la URL con el ticker (suponiendo que A4 es una variable con el ticker)
  ticke = "AAPL" 
  url = f"https://finance.yahoo.com/quote/{ticke}/analysis?ltr=1"

  # Añadir un User-Agent a la solicitud para simular una solicitud desde un navegador
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  }

  try:
      # Realizar la solicitud GET con los encabezados definidos
      response = requests.get(url, headers=headers)

      # Verificar si la solicitud fue exitosa (código 200)
      if response.status_code == 200:
          # Parsear el contenido HTML con BeautifulSoup
          soup = BeautifulSoup(response.text, 'html.parser')
          
          # Encontrar la tabla deseada (suponiendo que es la sexta tabla en la página)
          tables = soup.find_all('table')
          if len(tables) >= 6:
              desired_table = tables[5]  # Acceder a la sexta tabla (índice 5 en Python)
              
              # Extraer el valor específico de la tabla (fila 6, columna 2)
              rows = desired_table.find_all('tr')
              if len(rows) >= 6:
                  cells = rows[5].find_all('td')  # Obtener la sexta fila (índice 5 en Python)
                  if len(cells) >= 2:
                      target_value = cells[1].text.strip()  # Acceder a la segunda columna (índice 1 en Python)
                      # print(target_value)
                      return target_value
                  else:
                      print("No hay suficientes celdas en la fila seleccionada")
              else:
                  print("No hay suficientes filas en la tabla")
          else:
              print("No se encontraron suficientes tablas en la página")
      else:
          print(f"La solicitud no fue exitosa. Código de respuesta: {response.status_code}")

  except requests.exceptions.RequestException as e:
      print(f"Error en la solicitud: {e}")


# growthEstimates()

def dfc():
  # Obtenemos la tasa de crecimiento de los FCF
  growthFCF = float(growthEstimates().replace('%', '')) / 100
  # print('Crecimiento de los FCF: ', growthFCF)
  
  # Indicamos la tasa de crecimiento perpetuo (g)
  g = 0.03
  
  # Obtenemos la tasa de descuento (WACC)
  wacc = waccCalculator()
  
  # Obtenemos el FCF del ultimo año de yahoo finance
  fcf = ticker.cashflow.iloc[0]
  i = 0
  last_year_fcf = fcf.iloc[i]
  while math.isnan(fcf.iloc[i]):
    i += 1
    last_year_fcf = fcf.iloc[i]
  print('FCF: ', last_year_fcf)
  
  # Calculamos el flujo de caja libre para los prozimos 5 años
  FCFn = []
  for i in range(1, 6):
    last_year_fcf = last_year_fcf * (1 + growthFCF)
    FCFn.append(last_year_fcf)
  print('FCFn: ', FCFn)
  
  # Calculo el valor terminal
  terminal_value = (FCFn[-1] * (1 + g)) / (wacc - g)
  print('Valor terminal: ', terminal_value)
  
  # Calculo el valor de la empresa
  # 1. actualizo el ultimo valor del FCFn sumandole el valor terminal
  print('FCFn: ', FCFn[-1])
  FCFn[-1] = FCFn[-1] + terminal_value
  print('FCFn actualizado: ', FCFn)
  
  # 2. Calculo el valor de la empresa (realizo el calculo usando VNA)
  enterprise_value = 0
  for i in range(0, 5):
    # print(FCFn[i])
    enterprise_value += FCFn[i] / ((1 + wacc) ** (i + 1))
    # print('Valor de la empresa: ', enterprise_value)
  print('Valor de la empresa: ', enterprise_value)
  
  # Obtenemos el Cash. Cash Equivalents & Short Term Investments de yahoo finance
  cash = ticker.balance_sheet.loc['Cash Cash Equivalents And Short Term Investments']
  i = 0
  last_year_cash = cash.iloc[i]
  while math.isnan(cash.iloc[i]):
    i += 1
    last_year_cash = cash.iloc[i]
  print('Cash: ', last_year_cash)
  
  # Hacemos el ajuste para obtener el valor de la empresa
  equity_value = enterprise_value + last_year_cash - last_year_total_debt
  print('Valor de la empresa: ', equity_value)
  
  
  # Obtenemos las acciones en circulación (shares outstanding) de yahoo finance
  shares_outstanding = ticker.info['sharesOutstanding']
  print('Acciones en circulación: ', shares_outstanding)
  
  # Calculamos el valor intrínseco de la acción
  intrinsic_value = equity_value / shares_outstanding
  print('Valor intrínseco de la acción: ', intrinsic_value)
  
  # Obtenemos el precio de la acción de yahoo finance
  price = ticker.info['regularMarketPreviousClose']
  print('Precio de la acción: ', price)
  
  # Calulamos la diferencia entre el precio de la acción y el valor intrínseco de la acción
  difference = intrinsic_value / price - 1
  print('Diferencia: ', format((difference * 100), '.2f'), '%')
dfc()