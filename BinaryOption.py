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
                 delta_max: float = 10000,
                 pricing_method: str = 'BS',
                 annual_basis: int = 365):
        BlackScholes.__init__(self, spot, strike, rate, dividend, maturity, volatility, annual_basis)
        self.__payoff = payoff
        self.__delta_max = delta_max
        self.__pricing_method = pricing_method
        self.__typ = typ
        self.__rep = rep
        self.__record = pd.DataFrame(columns=['Type',
                                                'Spot',
                                                'Strike',
                                                'Rate',
                                                'Dividend',
                                                'Maturity',
                                                'Volatility',
                                                'Price_digital',
                                                'Price_spread',
                                                'Delta_digital',
                                                'Delta_spread',
                                                'Gamma_digital',
                                                'Gamma_spread',
                                                'Vega_digital',
                                                'Vega_spread',
                                                'Theta_digital',
                                                'Theta_spread',
                                                'Rho_digital',
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
                return self.delta_digital_call_bs(self.payoff) * self.spot / (self.price_digital * 100)
            if self.__typ == 'P':
                return self.delta_digital_put_bs(self.payoff) * self.spot / (self.price_digital * 100)
            if self.__typ == 'P':
                return self.delta_digital_put_bs(self.payoff)

    @property
    def price_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C': #Bull Spread
                #print(f'HERE km: {self.rep_option_km("Bull").price}')
                #print(f'HERE k: {self.rep_option_k().price}')
                return (self.rep_option_km('Bull').price - self.rep_option_k().price) * self.delta_max
            if self.__typ == 'P': #Bear Spread
                return (self.rep_option_km('Bear').price - self.rep_option_k().price) * self.delta_max

    @property
    def delta_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').delta - self.rep_option_k().delta) * self.delta_max * self.spot \
                       / (self.price_spread * 100)
            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').delta - self.rep_option_k().delta) * self.delta_max * self.spot \
                       / (self.price_spread * 100)

    @property
    def gamma_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.gamma_digital_call_bs(self.payoff) * self.delta_max \
                       * (self.spot ** 2) / (self.price_digital * 10000)
            if self.__typ == 'P':
                return self.gamma_digital_put_bs(self.payoff)

    @property
    def gamma_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').gamma - self.rep_option_k().gamma) * self.delta_max \
                       * (self.spot ** 2) / (self.price_spread * 10000)

            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').gamma - self.rep_option_k().gamma) * self.delta_max \
                       * (self.spot ** 2) / (self.price_spread * 10000)
    @property
    def vega_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.vega_digital_call_bs
            if self.__typ == 'P':
                return self.vega_digital_put_bs(self.payoff)

    @property
    def vega_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').vega - self.rep_option_k().vega) * self.delta_max \
                        * 10000 /self.price_spread

            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').vega - self.rep_option_k().vega) * self.delta_max \
                        * 10000 / self.price_spread

    @property
    def theta_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.theta_digital_call_bs
            if self.__typ == 'P':
                return self.theta_digital_put_bs

    @property
    def theta_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').theta - self.rep_option_k().theta) * self.delta_max \
                        * 10000 /self.price_spread
            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').theta - self.rep_option_k().theta) * self.delta_max \
                        * 10000 /self.price_spread

    @property
    def rho_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.rho_digital_call_bs
            if self.__typ == 'P':
                return self.rho_digital_put_bs(self.payoff)

    @property
    def rho_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').rho - self.rep_option_k().rho) * self.delta_max \
                        * 10000 /self.price_spread

            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').rho - self.rep_option_k().rho) * self.delta_max \
                        * 10000 /self.price_spread

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

    def recorder(self, date: str = "18/03/2022"):
        li = [self.typ,
                self.spot,
                self.strike,
                self.rate,
                self.dividend,
                self.maturity,
                self.volatility,
                self.price_digital,
                self.price_spread,
                self.delta_digital,
                self.delta_spread,
                self.gamma_digital,
                self.gamma_spread,
                self.vega_digital,
                self.vega_spread,
                self.theta_digital,
                self.theta_spread,
                self.rho_digital,
                self.rho_spread]

        self.__record.loc[len(self.__record)] = li
        idx = list(self.__record.index)
        idx[-1] = date
        self.__record.index = idx

    def setter(self, inp: tuple, date: str):
        self.spot = inp[0]
        self.rate = inp[1]
        self.dividend = inp[2]
        self.volatility = inp[3]
        self.maturity = inp[4]
        self.recorder(date)

