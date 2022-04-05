from VanillaOption import VanillaOption
from BlackScholes import BlackScholes
import pandas as pd


class BinaryOption(BlackScholes):
    def __init__(self,
                 spot: float,
                 strike: int,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 volatility: float = 0,
                 typ: str = 'C',
                 rep: str = 'C',
                 payoff: float = 1,
                 delta_max: float = 1,
                 pricing_method: str = 'BS',
                 annual_basis: int = 365):
        BlackScholes.__init__(self, spot, strike, rate, dividend, maturity, volatility, annual_basis)
        self.__payoff = payoff
        self.__delta_max = delta_max
        self.__pricing_method = pricing_method
        self.__typ = typ
        self.__rep = rep
        self.__record = pd.DataFrame(columns=['Spot',
                                              'Strike',
                                              'Rate',
                                              'Dividend',
                                              'Maturity',
                                              'Volatility',
                                              'Price_digital',
                                              'Price_spread',
                                              'Delta_digital',
                                              'Delta_spread',
                                              'Delta_max',
                                              'Gamma_spread',
                                              'Vega_spread',
                                              'Theta_spread',
                                              'Rho_spread'])
        self.recorder()

    def __str__(self):
        return 'Binary Option'

    @property
    def record(self):
        return self.__record

    @property
    def typ(self) -> str:
        return self.__typ

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
    def payoff(self) -> float:
        return self.__payoff

    @payoff.setter
    def payoff(self, payoff):
        self.__payoff = payoff

    @property
    def delta_max(self) -> float:
        return self.__delta_max

    @delta_max.setter
    def delta_max(self, delta_max):
        self.__delta_max = delta_max

    @property
    def pricing_method(self) -> str:
        return self.__pricing_method

    @pricing_method.setter
    def pricing_method(self, pricing_method):
        self.__pricing_method = pricing_method

    @property
    def overhedge_spread(self):
        return self.payoff / self.delta_max

    @property
    def price_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.price_call_digital_bs(self.payoff)
            if self.__typ == 'P':
                return self.price_put_digital_bs(self.payoff)

    @property
    def delta_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_digital_call_bs

    @property
    def price_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C': #Bull Spread
                #print(f'HERE km: {self.rep_option_km("Bull").price}')
                #print(f'HERE k: {self.rep_option_k().price}')
                return (self.rep_option_km('Bull').price - self.rep_option_k().price) * self.delta_max
            if self.__typ == 'P': #Bear Sprad
                return (self.rep_option_km('Bear').price - self.rep_option_k().price) * self.delta_max

    @property
    def delta_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').delta - self.rep_option_k().delta) * self.delta_max
            if self.__typ == 'P':  # Bear Sprad
                return (self.rep_option_km('Bear').delta - self.rep_option_k().delta) * self.delta_max

    @property
    def gamma_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').gamma - self.rep_option_k().gamma) * self.delta_max
            if self.__typ == 'P':  # Bear Sprad
                return (self.rep_option_km('Bear').gamma - self.rep_option_k().gamma) * self.delta_max

    @property
    def vega_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').vega - self.rep_option_k().vega) * self.delta_max
            if self.__typ == 'P':  # Bear Sprad
                return (self.rep_option_km('Bear').vega - self.rep_option_k().vega) * self.delta_max

    @property
    def theta_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').theta - self.rep_option_k().theta) * self.delta_max
            if self.__typ == 'P':  # Bear Sprad
                return (self.rep_option_km('Bear').theta - self.rep_option_k().theta) * self.delta_max

    @property
    def rho_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').rho - self.rep_option_k().rho) * self.delta_max
            if self.__typ == 'P':  # Bear Sprad
                return (self.rep_option_km('Bear').rho - self.rep_option_k().rho) * self.delta_max



    ############################################### REPLICATION
    def rep_option_k(self) -> VanillaOption:
        return VanillaOption(self.spot,
                             self.strike,
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__rep,
                             self.volatility)

    def rep_option_km(self, b):
        if b == "Bear":
            b = self.strike + self.overhedge_spread
        elif b == "Bull":
            b = self.strike - self.overhedge_spread
        return VanillaOption(self.spot,
                             b,
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__rep,
                             self.volatility)

    def recorder(self):
        li = [self.spot,
                self.strike,
                self.rate,
                self.dividend,
                self.maturity,
                self.volatility,
                self.price_digital,
                self.price_spread,
                self.delta_digital,
                self.delta_spread,
                self.delta_max,
                self.gamma_spread,
                self.vega_spread,
                self.theta_spread,
                self.rho_spread]

        self.__record.loc[self.__record.shape[0]] = li

    def setter(self, inp: tuple):
        self.spot = inp[0]
        self.rate = inp[1]
        self.dividend = inp[2]
        self.volatility = inp[3]
        self.maturity = inp[4]
        self.recorder()

