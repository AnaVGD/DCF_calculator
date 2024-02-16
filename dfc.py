import yfinance as yf
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import pandas as pd
# from alpha_vantage.timeseries import TimeSeries

# ts = TimeSeries(key='2TRGKH45LL2XZRE3',rapidapi=True)


balanceSheet = {}
info = {}
financials = {}
incomeStmt = {}
cashFlow = {}


# Obtenemos el valor de la deuda total (total debt) del ultimo año de yahoo finance
def getTotalDebt():
  d = balanceSheet.loc['Total Debt']
  i = 0
  last_year_total_debt = d.iloc[i]
  while (math.isnan(d.iloc[i]) and i < len(d) - 1):
    i += 1
    last_year_total_debt = d.iloc[i]
  return last_year_total_debt


#### Calcular WACC ####
def waccCalculator(ticker, rf, rm):
  
  last_year_total_debt = getTotalDebt()

  # Obtenemos el riesgo sistemático (beta) de la acción de yahoo finance
  beta = 1
  try:
    beta = info['beta']
  except Exception as e:
    return 'No se pudo obtener el beta de la acción'
  # print('Beta: ', beta)
    

  # Calculamos el costo del capital de los fondos propios (ke)
  ke = rf + (beta * (rm - rf))
  # print('Costo del capital de los fondos propios: ', ke)

  # Obtenemos la capitalización bursátil (market cap) del ultimo año de yahoo finance
  try:
    e = info['marketCap']
  except:
    return 'No se pudo obtener la capitalización bursátil de la acción'
  # print('Capitalización bursátil: ', e)

  # 7. Calculamos la deuda total (E + D)
  total_debt_ED = e + last_year_total_debt
  # print('Deuda total: ', total_debt_ED)

  # 8. Calculamos el total de los fondos propios (ke * (E / (E + D)))
  total_equity = ke * (e / total_debt_ED)
  # print('Total de los fondos propios: ', format((total_equity * 100), '.2f'), '%')
  # print('')

  # Calculo del coste de la deuda
  # Obtenemos el gasto por interese (Interest Expense) del ultimo año de yahoo finance
  interest_expense = 0
  # print(financials.loc['Interest Expense'])
  try:
    interest_expense = financials.loc['Interest Expense']
    i = 0
    last_year_interest_expense = interest_expense.iloc[i]
    while math.isnan(interest_expense.iloc[i]):
      i += 1
      last_year_interest_expense = interest_expense.iloc[i]
  except:
    return 'No se pudo obtener el gasto por intereses de la acción'
  # print('Gasto por intereses: ', last_year_interest_expense)

  # Obtener la deuda a corto plazo (current debt) del ultimo año de yahoo finance
  current_debt = 0
  try:
    current_debt = balanceSheet.loc['Current Debt And Capital Lease Obligation']
    i = 0
    last_year_current_debt = current_debt.iloc[i]
    while math.isnan(current_debt.iloc[i]):
      i += 1
      last_year_current_debt = current_debt.iloc[i]
  except:
    return 'No se pudo obtener la deuda a corto plazo de la acción'
  # print('Deuda a corto plazo: ', last_year_current_debt)

  # 3. obtener la deuda a largo plazo (long term debt) del ultimo año de yahoo finance
  try:
    long_term_debt = balanceSheet.loc['Long Term Debt']
    i = 0
    last_year_long_term_debt = long_term_debt.iloc[i]
    while math.isnan(long_term_debt.iloc[i]):
      i += 1
      last_year_long_term_debt = long_term_debt.iloc[i]
  except:
    return 'No se pudo obtener la deuda a largo plazo de la acción'
  # print('Deuda a largo plazo: ', last_year_long_term_debt)

  # 4. Obtener el coste de la deuda financiera (kd)
  kd = (last_year_interest_expense / (last_year_current_debt + last_year_long_term_debt))
  # print('Coste de la deuda financiera: ', format((kd * 100), '.2f'), '%')

  # 5. Obtener el ingreso por gastos de impuestos (tax Provision) del ultimo año de yahoo finance
  try:
    tax_provision = incomeStmt.loc['Tax Provision']
    i = 0
    last_year_tax_provision = tax_provision.iloc[i]
    while math.isnan(tax_provision.iloc[i]):
      i += 1
      last_year_tax_provision = tax_provision.iloc[i]
  except:
    return 'No se pudo obtener el ingreso por gastos de impuestos de la acción'
  # print('Ingreso por gastos de impuestos: ', last_year_tax_provision)

  # 6. Obtener el ingreso antes de impuestos (Pretax Income) del ultimo año de yahoo finance
  try:
    pretax_income = incomeStmt.loc['Pretax Income']
    i = 0
    last_year_pretax_income = pretax_income.iloc[i]
    while math.isnan(pretax_income.iloc[i]):
      i += 1
      last_year_pretax_income = pretax_income.iloc[i]
  except:
    return 'No se pudo obtener el ingreso antes de impuestos de la acción'
  # print('Ingreso antes de impuestos: ', last_year_pretax_income)

  # 7. Calculo la tasa impositiva (T)
  t = last_year_tax_provision / last_year_pretax_income
  # print('Tasa impositiva: ', format((t * 100), '.2f'), '%')

  # 8. Calculo el coste de la deuda
  total_debt_cost = kd * (1 - t) * ( last_year_total_debt / total_debt_ED)
  # print('Coste de la deuda: ', format((total_debt_cost * 100), '.2f'), '%')

  #### Calculo del WACC ####
  # 1. Calculo el WACC
  wacc = total_equity + total_debt_cost
  # print('\nWACC: ', format((wacc * 100), '.2f'), '%')
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
                      return("No hay suficientes celdas en la fila seleccionada")
              else:
                  return("No hay suficientes filas en la tabla")
          else:
              return("No se encontraron suficientes tablas en la página")
      else:
          return(f"La solicitud no fue exitosa. Código de respuesta: {response.status_code}")

  except requests.exceptions.RequestException as e:
      return(f"Error en la solicitud: {e}")

def getEbitda(ticker):
  global incomeStmt
  try:
    ebitda = incomeStmt.loc['EBITDA']
  except:
    return 'No se pudo obtener el EBITDA de la acción'
  i = 0
  last_year_ebitda = ebitda.iloc[i]
  while math.isnan(ebitda.iloc[i]):
    i += 1
    last_year_ebitda = ebitda.iloc[i]
  return last_year_ebitda

def getEarnings(ticker):
  global incomeStmt
  try:
    grossProfitArr = incomeStmt.loc['Gross Profit']
    totalRevenueArr = incomeStmt.loc['Total Revenue']
  except:
    return 'No se pudo obtener las ganancias de la acción'
  i = 0
  grossProfit = grossProfitArr.iloc[i]
  totalRevenue = totalRevenueArr.iloc[i]
  while math.isnan(grossProfitArr.iloc[i]):
    i += 1
    grossProfit = grossProfitArr.iloc[i]
  while math.isnan(totalRevenueArr.iloc[i]):
    i += 1
    totalRevenue = totalRevenueArr.iloc[i]
  return (grossProfit / totalRevenue) * 100

def getRoe(ticker):
  global balanceSheet
  global incomeStmt
  try:
    netIncome = incomeStmt.loc['Net Income']
    i = 0
    last_year_net_income = netIncome.iloc[i]
    while math.isnan(netIncome.iloc[i]):
      i += 1
      last_year_net_income = netIncome.iloc[i]
  except:
    return 'No se pudo obtener el net income de la acción'
  try:
    equity = balanceSheet.loc['Stockholders Equity']
    i = 0
    last_year_equity = equity.iloc[i]
    while math.isnan(equity.iloc[i]):
      i += 1
      last_year_equity = equity.iloc[i]
  except:
    return 'No se pudo obtener el equity de la acción'
  return (last_year_net_income / last_year_equity) * 100

def arrDfc(tickerStr, g, rf, rm, hasEbitda, hasEarnings, hasRoe):
  global balanceSheet
  global info
  global financials
  global incomeStmt
  global cashFlow
  finalResult = []
  print('Ticker: ', tickerStr)
  
  for i in range(0, len(tickerStr)):
    if (tickerStr[i] != ''):
      ticker = yf.Ticker(tickerStr[i])
      ebitda = 0
      earnings = 0
      roe = 0
      
      balanceSheet = getBalanceSheet(ticker)
      info = getInfo(ticker)
      financials = getFinancials(ticker)
      incomeStmt = getIncomeStmt(ticker)
      cashFlow = getCashFlow(ticker)
      
      if (type(balanceSheet) == str):
        return balanceSheet
      if (type(info) == str):
        return info
      if (type(financials) == str):
        return financials
      if (type(incomeStmt) == str):
        return incomeStmt
      if (type(cashFlow) == str):
        return cashFlow

      
      # print(getRoe(ticker))
    
      if (hasEbitda):
        ebitda = getEbitda(ticker)
        # print('EBITDA: ', ebitda)
      
      if (hasEarnings):
        earnings = ((format(getEarnings(ticker), '.2f')), ' %')
        # print('Earnings: ', earnings)
      
      if (hasRoe):
        roe = (format(getRoe(ticker), '.2f')) + ' %'
        # print('ROE: ', roe)
        
      options = [ebitda, earnings, roe]
      finalsOptions = []
      for option in options:
        if (option != 0):
          finalsOptions.append(option)

      
      resultDFC = dfc(ticker, g, rf, rm)
      if (type(resultDFC) == str):
        return resultDFC

      arrayWithUSD = ['$ ' + str(value) for value in resultDFC[2]]
      finalResult.append([tickerStr[i], resultDFC[0], resultDFC[1]] + arrayWithUSD + [resultDFC[3]] + [resultDFC[4]] + [resultDFC[5]] + [resultDFC[6]] + finalsOptions)

  return finalResult

def dfc(ticker, g, rf, rm):
  global balanceSheet
  global info
  global financials
  global incomeStmt
  global cashFlow
  
  last_year_total_debt = getTotalDebt()
  
  # Obtenemos la tasa de crecimiento de los FCF
  growthFCF = growthEstimates()
  # growthFCF = float(growthFCF.replace('%', '')) / 100
  try:
    growthFCF = float(growthFCF.replace('%', '')) / 100
  except:
    return growthFCF
  

  
  # Obtenemos la tasa de descuento (WACC)
  wacc = waccCalculator(ticker, rf, rm)
  # print('WACC: ', wacc)
  if (type(wacc) != float):
    return wacc
  
  # Obtenemos el FCF del ultimo año de yahoo finance
  try:
    fcf = cashFlow.iloc[0]
    i = 0
    last_year_fcf = fcf.iloc[i]
    while math.isnan(fcf.iloc[i]):
      i += 1
      last_year_fcf = fcf.iloc[i]
    printFCF = last_year_fcf
  except:
    return 'No se pudo obtener el FCF de la acción'
  
  # Calculamos el flujo de caja libre para los prozimos 5 años
  FCFn = []
  for i in range(1, 6):
    last_year_fcf = last_year_fcf * (1 + growthFCF)
    FCFn.append(int(format(last_year_fcf, '.0f')))
  
  # Calculo el valor terminal
  terminal_value = (FCFn[-1] * (1 + g)) / (wacc - g)
  
  # Calculo el valor de la empresa
  # Actualizo el ultimo valor del FCFn sumandole el valor terminal
  FCFn[-1] = int(format(FCFn[-1] + terminal_value, '.0f'))
  
  # Calculo el valor de la empresa (realizo el calculo usando VNA)
  enterprise_value = 0
  for i in range(0, 5):
    enterprise_value += FCFn[i] / ((1 + wacc) ** (i + 1))
  
  # Obtenemos el Cash. Cash Equivalents & Short Term Investments de yahoo finance
  try:
    cash = balanceSheet.loc['Cash Cash Equivalents And Short Term Investments']
    i = 0
    last_year_cash = cash.iloc[i]
    while math.isnan(cash.iloc[i]):
      i += 1
      last_year_cash = cash.iloc[i]
  except:
    return 'No se pudo obtener el Cash de la acción'
  
  # Hacemos el ajuste para obtener el valor de la empresa
  equity_value = enterprise_value + last_year_cash - last_year_total_debt

  # Obtenemos las acciones en circulación (shares outstanding) de yahoo finance
  try:
    shares_outstanding = info['sharesOutstanding']
  except:
    return 'No se pudo obtener las acciones en circulación de la acción'

  
  # Calculamos el valor intrínseco de la acción
  intrinsic_value = equity_value / shares_outstanding
  
  # Obtenemos el precio de la acción de yahoo finance
  try:
    price = info['regularMarketPreviousClose']
  except:
    return 'No se pudo obtener el precio de la acción'
  
  # Calulamos la diferencia entre el precio de la acción y el valor intrínseco de la acción
  difference = intrinsic_value / price - 1
  
  # return format((intrinsic_value), '.2f')
  # print(tickerYf, wacc, printFCF, FCFn, equity_value, equity_value)
  return [(format((wacc * 100), '.2f') + ' %'), ('$ ' + str(printFCF)), FCFn, ('$ ' + format(equity_value, '.0f')), price, format(intrinsic_value, '.2f'), format((difference * 100), '.2f')]


def getBalanceSheet(ticker):
  try:
    return ticker.balance_sheet
  except:
    return 'No se pudo obtener el balance de la acción'

def getIncomeStmt(ticker):
  try:
    return ticker.income_stmt
  except:
    return 'No se pudo obtener el estado de resultados de la acción'

def getInfo(ticker):
  try:
    return ticker.info
  except:
    return 'No se pudo obtener la información de la acción'

def getCashFlow(ticker):
  try:
    return ticker.cashflow
  except:
    return 'No se pudo obtener el flujo de caja de la acción'

def getFinancials(ticker):
  try:
    return ticker.financials
  except:
    return 'No se pudo obtener los estados financieros de la acción'

