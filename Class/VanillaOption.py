import pandas as pd

from Class.BlackScholes import BlackScholes


class VanillaOption(BlackScholes):
    """
    Annual Basis default 365
    Annual Volatility: 0.16 for 16% annually
    Annual Rate: 0.03 for 3% annually
    Annual Dividend: 0.05 for 5% annually
    Maturity in days

    Pricing methods:
    BS --> Black & Scholes + Greeks
    """

    def __init__(self,
                 spot: float,
                 strike: float,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 typ: str = 'C',
                 volatility: float = 0,
                 pricing_method: str = 'BS',
                 annual_basis: int = 365):
        """
        :param spot: spot price
        :param strike: strike price
        :param rate: risk free rate 0.05 corresponds to 5%
        :param dividend: dividend yield 0.01 corresponds to 1%
        :param maturity: maturity in days
        :param typ: 'C': Call / 'P': Put
        :param volatility: volatility 0.16 corresponds to 16%
        :param pricing_method: 'BS': Black&Scholes
        """
        BlackScholes.__init__(self, spot, strike, rate, dividend, maturity, volatility, annual_basis)
        self._inception_date = "12/03/2022"
        self.__typ = typ
        self.__pricing_method = pricing_method
        self.__record = pd.DataFrame(columns=['Typ',
                                                'Spot',
                                                'Strike',
                                                'Rate',
                                                'Dividend',
                                                'Maturity',
                                                'Volatility',
                                                'Price',
                                                'Delta',
                                                'Gamma',
                                                'Vega',
                                                'Theta',
                                                'Rho'])
        #self.recorder()

    @property
    def record(self):
        return self.__record

    @property
    def spot(self) -> float:
        return self._spot

    @spot.setter
    def spot(self, spot):
        self._spot = spot

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    @property
    def dividend(self) -> float:
        return self._dividend

    @dividend.setter
    def dividend(self, dividend):
        self._dividend = dividend

    @property
    def maturity(self) -> int:
        return self._maturity

    @maturity.setter
    def maturity(self, maturity):
        self._maturity = maturity

    @property
    def volatility(self) -> float:
        return self._volatility

    @volatility.setter
    def volatility(self, volatility):
        self._volatility = volatility

    @property
    def pricing_method(self) -> str:
        return self.__pricing_method

    @property
    def price(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.price_call_bs
            if self.__typ == 'P':
                return self.price_put_bs

    @property
    def delta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_call_bs
            if self.__typ == 'P':
                return self.delta_put_bs

    @property
    def theta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.theta_call_bs
            if self.__typ == 'P':
                return self.theta_put_bs

    @property
    def gamma(self) -> float:
        if self.__pricing_method == "BS":
            return self.gamma_bs

    @property
    def vega(self) -> float:
        if self.__pricing_method == "BS":
            return self.vega_bs

    @property
    def rho(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.rho_call_bs
            if self.__typ == 'P':
                return self.rho_put_bs

    # def recorder(self, date: str = "12/03/2022"):
    #     li = [self.__typ,
    #             self.spot,
    #             self.strike,
    #             self.rate,
    #             self.dividend,
    #             self.maturity,
    #             self.volatility,
    #             self.price,
    #             self.delta,
    #             self.gamma,
    #             self.vega,
    #             self.theta,
    #             self.rho]
    #
    #     self.__record.loc[self.__record.shape[0]] = li
    #     idx = list(self.__record.index)
    #     idx[-1] = date
    #     self.__record.index = idx
    #
    # def setter(self, inp: tuple, date: str):
    #     self.spot = inp[0]
    #     self.rate = inp[1]
    #     self.dividend = inp[2]
    #     self.maturity = inp[3]
    #     self.volatility = inp[4]
    #     self.recorder(date)

