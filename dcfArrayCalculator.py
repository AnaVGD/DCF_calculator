import yfinance as yf
from dcfCalculator import DcfCalculator


class DcfArrayCalculator:
    def __init__(self):
        """Inicializa el objeto DcfArrayCalculator."""
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

    def arrDcf(self, tickerStr, g, rf, rm, hasEbitda, hasEarnings, hasRoe, hasPer):
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
            dcfCalculator = DcfCalculator(yf.Ticker(ticker))

            values = [
                (hasEbitda, dcfCalculator.getEbitda, False, False),
                (hasEarnings, dcfCalculator.getEarnings, True, True),
                (hasRoe, dcfCalculator.getRoe, True, True),
                (hasPer, dcfCalculator.getPer, True, False),
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

            resultDCF = dcfCalculator.dcf(ticker, g, rf, rm)
            if isinstance(resultDCF, str):
                finalResult.append([ticker.upper(), "Error"])
            else:
                arrayWithUSD = [
                    ("$ " + "{:,.0f}".format(value).replace(",", "."))
                    for value in resultDCF[2]
                ]
                finalResult.append(
                    [ticker.upper(), resultDCF[0], resultDCF[1]]
                    + arrayWithUSD
                    + resultDCF[3:]
                    + finalsOptions
                )

        return finalResult
