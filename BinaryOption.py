from VanillaOption import VanillaOption
from BlackScholes import BlackScholes
import pandas as pd
import Smile


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
                 annual_basis: int = 365,
                 smile_active: bool = True):
        BlackScholes.__init__(self, spot, strike, rate, dividend, maturity, volatility, annual_basis)
        self._inception_date = "12/03/2022"
        self.__payoff = payoff
        self.__delta_max = delta_max
        self.__pricing_method = pricing_method
        self.__typ = typ
        self.__rep = rep
        self.__smile_active = smile_active
        self.__volatility_km_bear = 0
        self.__volatility_km_bull = 0
        self.__strike_km_bear = self.strike + self.overhedge_spread
        self.__strike_km_bull = self.strike - self.overhedge_spread
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
        if not self.__smile_active:
            pass
        else:
            self.volatility = self.smile(self._inception_date, self.strike)
            self.__volatility_km_bear = self.smile(self._inception_date, self.__strike_km_bear)
            self.__volatility_km_bull = self.smile(self._inception_date, self.__strike_km_bull)
        self.recorder(self._inception_date)

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
    def price_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C': #Bull Spread
                #print(f'HERE km: {self.rep_option_km("Bull").price}')
                #print(f'HERE k: {self.rep_option_k().price}')
                return (self.rep_option_km('Bull').price - self.rep_option_k().price) * self.delta_max
            if self.__typ == 'P': #Bear Spread
                return (self.rep_option_km('Bear').price - self.rep_option_k().price) * self.delta_max

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
                return self.gamma_digital_call_bs(self.payoff) * (self.spot ** 2) / (self.price_digital * 10000)
            if self.__typ == 'P':
                return self.gamma_digital_put_bs(self.payoff) * self.delta_max * (self.spot ** 2) / (self.price_digital * 10000)

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
                return self.vega_digital_call_bs(self.payoff) * 10000 / self.price_digital
            if self.__typ == 'P':
                return self.vega_digital_put_bs(self.payoff) * 10000 / self.price_digital

    @property
    def vega_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return (self.rep_option_km('Bull').vega - self.rep_option_k().vega) * self.delta_max \
                        * 10000 / self.price_spread

            if self.__typ == 'P':  # Bear Spread
                return (self.rep_option_km('Bear').vega - self.rep_option_k().vega) * self.delta_max \
                        * 10000 / self.price_spread

    @property
    def theta_digital(self) -> float: #FAUX
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.theta_digital_call_bs(self.payoff) * 10000 / self.price_digital
            if self.__typ == 'P':
                return self.theta_digital_put_bs(self.payoff) * 10000 / self.price_digital

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
                return self.rho_digital_call_bs(self.payoff) * 10000 / self.price_digital
            if self.__typ == 'P':
                return self.rho_digital_put_bs(self.payoff) * 10000 / self.price_digital

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
            km = self.__strike_km_bear
            if self.__smile_active:
                volm = self.__volatility_km_bear
            else:
                volm = self.volatility
        else:
            km = self.__strike_km_bull
            if self.__smile_active:
                volm = self.__volatility_km_bull
            else:
                volm = self.volatility
        return VanillaOption(self.spot,
                             km,
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__rep,
                             volm)

    def recorder(self, date: str):
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
        self.maturity -= 1
        if not self.__smile_active:
            self.volatility = inp[3]
        else:
            self.volatility = self.smile(date, self.strike)
            self.__volatility_km_bear = self.smile(date, self.__strike_km_bear)
            self.__volatility_km_bull = self.smile(date, self.__strike_km_bull)
        self.recorder(date)
        return self.maturity


####################### SMILE

    def smile(self, date, strike):
        smile = Smile.Smile(self.spot, self.maturity, date)
        volatility = smile.volatility(strike)
        return volatility



