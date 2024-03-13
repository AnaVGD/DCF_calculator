import math
import requests
from bs4 import BeautifulSoup

"""
Documentación de la clase FinanceAnalyzer
"""


class DcfCalculator:
    def __init__(self, ticker=None):
        """
        Inicializa el objeto FinanceAnalyzer con los datos financieros del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.
        """
        self.balanceSheet = self.getBalanceSheet(ticker)
        """El balance de la acción."""
        self.info = self.getInfo(ticker)
        """La información básica de la acción."""
        self.financials = self.getFinancials(ticker)
        """Los estados financieros de la acción."""
        self.incomeStmt = self.getIncomeStmt(ticker)
        """El estado de ingresos de la acción."""
        self.cashFlow = self.getCashFlow(ticker)
        """El flujo de efectivo de la acción."""

    def getAttribute(self, ticker, attribute, error_message):
        """
        Obtiene los datos de yahoo finance

        Args:
            ticker (str): El símbolo de ticker de la acción.
            attribute (str): El nombre del atributo a obtener.
            error_message (str): El mensaje de error a mostrar si el atributo no se puede obtener.

        Returns:
            obj: El valor del atributo.
        """
        try:
            return getattr(ticker, attribute)
        except:
            raise Exception(error_message)

    def getFinancials(self, ticker):
        """
        Obtiene los estados financieros del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            obj: Los estados financieros del ticker.
        """
        return self.getAttribute(
            ticker,
            "financials",
            "No se pudo obtener los estados financieros de la acción",
        )

    def getBalanceSheet(self, ticker):
        """
        Obtiene el balance de la acción del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            obj: El balance de la acción.
        """
        return self.getAttribute(
            ticker, "balance_sheet", "No se pudo obtener el balance de la acción"
        )

    def getIncomeStmt(self, ticker):
        """
        Obtiene el estado de ingresos de la acción del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            obj: El estado de ingresos de la acción.
        """
        return self.getAttribute(
            ticker,
            "income_stmt",
            "No se pudo obtener el estado de los ingresos de la acción",
        )

    def getInfo(self, ticker):
        """
        Obtiene la información básica de la acción del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            obj: La información básica de la acción.
        """
        return self.getAttribute(
            ticker, "info", "No se pudo obtener la información de la acción"
        )

    def getCashFlow(self, ticker):
        """
        Obtiene el flujo de efectivo de la acción del ticker especificado.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            obj: El flujo de efectivo de la acción.
        """
        return self.getAttribute(
            ticker, "cashflow", "No se pudo obtener el flujo de caja de la acción"
        )

    def getEbitda(self):
        """
        Calcula el EBITDA de la acción.

        Returns:
            float: El EBITDA de la acción.
        """
        try:
            ebitda = self.getLastYearValue(self.incomeStmt, "EBITDA")
        except Exception as e:
            raise Exception("No se pudo obtener el EBITDA de la acción") from e
        return ebitda

    def getEarnings(self):
        """
        Calcula las ganancias de la acción.

        Returns:
            float: Las ganancias de la acción.
        """
        try:
            grossProfit = self.getLastYearValue(self.incomeStmt, "Gross Profit")
            totalRevenue = self.getLastYearValue(self.incomeStmt, "Total Revenue")
            return (grossProfit / totalRevenue) * 100
        except Exception as e:
            raise Exception("No se pudo obtener las ganancias de la acción") from e

    def getRoe(self):
        """
        Calcula el ROE (Return on Equity) de la acción.

        Returns:
            float: El ROE de la acción.
        """
        try:
            last_year_net_income = self.getLastYearValue(self.incomeStmt, "Net Income")
        except Exception as e:
            raise Exception("No se pudo obtener el net income de la acción") from e

        try:
            last_year_equity = self.getLastYearValue(
                self.balanceSheet, "Stockholders Equity"
            )
        except Exception as e:
            raise Exception("No se pudo obtener el equity de la acción") from e

        return (last_year_net_income / last_year_equity) * 100

    def getPer(self):
        """
        Obtiene el PER (Price to Earnings Ratio) de la acción.

        Returns:
            float: El PER de la acción.
        """
        try:
            return self.info["trailingPE"]
        except:
            raise Exception("No se pudo obtener el PER de la acción")

    def getLastYearValue(self, data, label):
        """
        Obtiene el valor del año pasado para una etiqueta de datos específica.

        Args:
            data (DataFrame): Los datos financieros.
            label (str): La etiqueta de datos específica.

        Returns:
            float: El valor del año pasado para la etiqueta de datos especificada.
        """
        try:
            value = data.loc[label]
            i = 0
            last_year_value = value.iloc[i]
            while math.isnan(value.iloc[i]):
                i += 1
                last_year_value = value.iloc[i]
            return last_year_value
        except:
            try:
                if label == "Current Debt And Capital Lease Obligation":
                    return self.getLastYearValue(data, "Current Deferred Liabilities")
            except:
                raise Exception(f"No se pudo obtener {label} de la acción")
            raise Exception(f"No se pudo obtener {label} de la acción")

    def getTotalDebt(self, balanceSheet):
        """
        Calcula la deuda total de la acción.

        Args:
            balanceSheet (DataFrame): El balance de la acción.

        Returns:
            float: La deuda total de la acción.
        """
        try:
            return self.getLastYearValue(balanceSheet, "Total Debt")
        except Exception as e:
            raise Exception("No se pudo obtener la deuda total de la acción") from e

    def getGrowthEstimates(self, ticker, option):
        """
        Obtiene las estimaciones de crecimiento para la acción.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            str: Las estimaciones de crecimiento.
        """
        try:
            if option == "yahoo":
                return self.getGrowthEstimatesYahoo(ticker)
            elif option == "zacks":
                return self.getGrowthEstimatesZacks(ticker)
            elif option == "seeking":
                return self.getGrowthEstimatesSeeking(ticker)

        except Exception as e:
            return str(e)

    def getGrowthEstimatesYahoo(self, ticker):
        """
        Obtiene las estimaciones de crecimiento para la acción de la webd e Yahoo Finance.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            str: Las estimaciones de crecimiento.
        """
        url = f"https://finance.yahoo.com/quote/{ticker}/analysis?ltr=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            desired_table = soup.find_all("table")[5]
            target_value = (
                desired_table.find_all("tr")[5].find_all("td")[1].text.strip()
            )
            return target_value
        except IndexError:
            raise Exception(
                "No se encontraron suficientes tablas, filas o celdas en la página"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la solicitud: {e}")

    def getGrowthEstimatesZacks(self, ticker):
        """
        Obtiene las estimaciones de crecimiento para la acción de la web de Zacks.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            str: Las estimaciones de crecimiento.
        """
        url = f"https://www.zacks.com/stock/quote/{ticker}?q={ticker}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            desired_table = soup.find_all("dl", class_="abut_bottom")
            # print(desired_table)
            target_value = desired_table[15].find_all("dd")[0].text.strip()
            # print(target_value)
            return target_value
        except IndexError:
            raise Exception(
                "No se encontraron suficientes tablas, filas o celdas en la página"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la solicitud: {e}")

    def getGrowthEstimatesSeeking(self, ticker):
        """
        Obtiene las estimaciones de crecimiento para la acción de la web de Seeking Alpha.

        Args:
            ticker (str): El símbolo de ticker de la acción.

        Returns:
            str: Las estimaciones de crecimiento.
        """
        url = f"https://seekingalpha.com/symbol/{ticker}/growth"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            # print(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            desired_table = soup.find_all("table")[0]
            target_value = (
                desired_table.find_all("tr")[11].find_all("td")[1].text.strip()
            )
            # print(target_value, 'hi')
            return target_value
        except IndexError:
            raise Exception(
                "No se encontraron suficientes tablas, filas o celdas en la página"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la solicitud: {e}")

    def waccCalculator(self, rf, rm):
        """
        Calcula el costo promedio ponderado del capital (WACC).

        Args:
            rf (float): Tasa libre de riesgo.
            rm (float): Retorno del mercado.

        Returns:
            float: El WACC calculado.
        """
        last_year_total_debt = self.getTotalDebt(self.balanceSheet)

        beta = self.info.get("beta", 1)

        ke = rf + (beta * (rm - rf))

        e = self.info.get("marketCap")
        if e is None:
            raise Exception(
                "No se pudo obtener la capitalización bursátil de la acción"
            )

        total_debt_ED = e + last_year_total_debt

        total_equity = ke * (e / total_debt_ED)

        last_year_interest_expense = self.getLastYearValue(
            self.financials, "Interest Expense"
        )

        last_year_current_debt = self.getLastYearValue(
            self.balanceSheet, "Current Debt And Capital Lease Obligation"
        )

        last_year_long_term_debt = self.getLastYearValue(
            self.balanceSheet, "Long Term Debt"
        )

        kd = last_year_interest_expense / (
            last_year_current_debt + last_year_long_term_debt
        )

        last_year_tax_provision = self.getLastYearValue(
            self.incomeStmt, "Tax Provision"
        )

        last_year_pretax_income = self.getLastYearValue(
            self.incomeStmt, "Pretax Income"
        )

        t = last_year_tax_provision / last_year_pretax_income

        total_debt_cost = kd * (1 - t) * (last_year_total_debt / total_debt_ED)

        return total_equity + total_debt_cost

    def dcf(self, tickerStr, g, rf, rm, option):
        """
        Calcula el valor intrínseco de una acción utilizando el modelo de descuento de flujos de efectivo (DCF).

        Args:
            tickerStr (str): El símbolo de ticker de la acción.
            g (float): Tasa de crecimiento a perpetuidad.
            rf (float): Tasa libre de riesgo.
            rm (float): Retorno del mercado.

        Returns:
            list: Una lista que contiene varios valores calculados.
        """
        try:
            last_year_total_debt = self.getTotalDebt(self.balanceSheet)
            growthFCF = self.getGrowthEstimates(tickerStr, option)
            printGrowthFCF = growthFCF
            try:
                growthFCF = float(growthFCF.replace("%", "")) / 100
            except:
                FCFGrow = self.cashFlow.iloc[0]
                growthFCF = (
                    (FCFGrow.iloc[0] / FCFGrow.iloc[-1]) ** (1 / len(FCFGrow))
                ) - 1
                printGrowthFCF = "{:.2f}%".format(growthFCF * 100)

            wacc = self.waccCalculator(rf, rm)
            if type(wacc) != float:
                raise Exception(wacc)

            last_year_fcf = self.getLastYearValue(self.cashFlow, "Free Cash Flow")
            printFCF = last_year_fcf

            FCFn = [
                int(format(last_year_fcf * (1 + growthFCF) ** i, ".0f"))
                for i in range(1, 6)
            ]

            terminal_value = (FCFn[-1] * (1 + g)) / (wacc - g)
            FNFnLast = FCFn[-1]
            FCFn[-1] = int(format(FCFn[-1] + terminal_value, ".0f"))

            enterprise_value = sum(
                [FCFn[i] / ((1 + wacc) ** (i + 1)) for i in range(5)]
            )

            last_year_cash = self.getLastYearValue(
                self.balanceSheet, "Cash Cash Equivalents And Short Term Investments"
            )

            equity_value = enterprise_value + last_year_cash - last_year_total_debt

            shares_outstanding = self.info["sharesOutstanding"]

            intrinsic_value = equity_value / shares_outstanding

            price = self.info["regularMarketPreviousClose"]

            difference = 100 + (((intrinsic_value - price) / price) * 100)

            FCFn.pop()
            FCFn.append(FNFnLast)

            return [
                (format((wacc * 100), ".2f") + " %"),
                ("$ " + "{:,.0f}".format(printFCF).replace(",", ".")),
                FCFn,
                printGrowthFCF,
                ("$ " + "{:,.0f}".format(equity_value, ".0f").replace(",", ".")),
                ("$ " + str(price)),
                ("$ " + format(intrinsic_value, ".2f")),
                (format((difference), ".2f") + "%"),
            ]
        except Exception as e:
            return str(e)


# DcfCalculator("STX").getGrowthEstimates("AAPL")
# DcfCalculator("STX").getGrowthEstimatesSeeking("AAPL")
