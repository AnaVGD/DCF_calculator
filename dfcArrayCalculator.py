import yfinance as yf
from dfcCalculator import DfcCalculator


class DfcArrayCalculator:
    def __init__(self):
        """Inicializa el objeto DfcArrayCalculator."""
        pass

    def getValue(self, ticker, method, format, percentage):
        """
        Obtiene el valor de un método específico y lo formatea según sea necesario.

        Args:
            ticker (str): El símbolo del ticker de la acción.
            method (method): El método para obtener el valor.
            format (bool): Indica si el valor debe ser formateado.
            percentage (bool): Indica si el valor es un porcentaje.

        Returns:
            obj: El valor obtenido.
        """
        try:
            value = method()
            if format:
                if percentage:
                    value = "{:.2f}%".format(value)
                else:
                    value = "{:,.2f}".format(value)
            return value
        except Exception as e:
            raise Exception(f"No se pudo obtener el valor de {ticker}\n {e}") from e

    def arrDfc(self, tickerStr, g, rf, rm, hasEbitda, hasEarnings, hasRoe, hasPer):
        """
        Calcula los valores DCF para una lista de tickers.

        Args:
            tickerStr (list): Lista de símbolos de ticker de las acciones.
            g (float): Tasa de crecimiento a perpetuidad.
            rf (float): Tasa libre de riesgo.
            rm (float): Retorno del mercado.
            hasEbitda (bool): Indica si se requiere el cálculo de EBITDA.
            hasEarnings (bool): Indica si se requiere el cálculo de las ganancias.
            hasRoe (bool): Indica si se requiere el cálculo de ROE.
            hasPer (bool): Indica si se requiere el cálculo de PER.

        Returns:
            list: Una lista que contiene los valores DCF calculados para cada ticker.
        """
        finalResult = []

        for ticker in filter(None, tickerStr):
            dfcCalculator = DfcCalculator(yf.Ticker(ticker))

            values = [
                (hasEbitda, dfcCalculator.getEbitda, False, False),
                (hasEarnings, dfcCalculator.getEarnings, True, True),
                (hasRoe, dfcCalculator.getRoe, True, True),
                (hasPer, dfcCalculator.getPer, True, False),
            ]

            finalsOptions = []
            for has_value, method, format, percentage in values:
                if has_value:
                    try:
                        value = self.getValue(ticker, method, format, percentage)
                        if value is not None:
                            finalsOptions.append(value)
                    except Exception as e:
                        print(e)
                        finalsOptions = ["Error"]
                        break

            resultDFC = dfcCalculator.dfc(ticker, g, rf, rm)
            if isinstance(resultDFC, str):
                print(resultDFC)
                finalResult.append([ticker.upper(), "Error"])
            else:
                arrayWithUSD = [
                    ("$ " + "{:,.0f}".format(value).replace(",", "."))
                    for value in resultDFC[2]
                ]
                finalResult.append(
                    [ticker.upper(), resultDFC[0], resultDFC[1]]
                    + arrayWithUSD
                    + resultDFC[3:]
                    + finalsOptions
                )

        return finalResult
