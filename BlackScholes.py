import numpy as np
from scipy.stats import norm


class BlackScholes:
    def __init__(self,
                 spot: float,
                 strike: float,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 volatility: float,
                 annual_basis: int = 365):
        """
        :param spot: spot price
        :param strike: strike price
        :param rate: risk free rate 0.05 corresponds to 5%
        :param dividend: dividend yield 0.01 corresponds to 1%
        :param maturity: maturity in days
        :param volatility: volatility 0.16 corresponds to 16%
        """
        self._spot = spot
        self.__strike = strike
        self._rate = rate
        self._dividend = dividend
        self._maturity = maturity
        self._volatility = volatility
        self.__annual_basis = annual_basis

    @property
    def spot(self) -> float:
        return self._spot

    @property
    def strike(self) -> float:
        return self.__strike

    @property
    def rate(self) -> float:
        return self._rate

    @property
    def dividend(self) -> float:
        return self._dividend

    @property
    def maturity(self) -> int:
        return self._maturity

    @property
    def volatility(self) -> float:
        return self._volatility

    @property
    def annual_basis(self) -> float:
        return self.__annual_basis

    @property
    def d1(self) -> float:
        """
        :return: the d1 of the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        sig = self._volatility
        t = self._maturity
        b = self.__annual_basis
        return (np.log(s / k) + (r - q + 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @property
    def d2(self) -> float:
        """
        :return: the d2 of the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        sig = self._volatility
        t = self._maturity
        b = self.__annual_basis
        return (np.log(s / k) + (r - q - 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @property
    def n_d1(self,) -> float:
        return norm.cdf(self.d1, 0, 1)

    @property
    def n_d2(self) -> float:
        return norm.cdf(self.d2, 0, 1)

    @property
    def d_n_d1(self) -> float:
        return norm.pdf(self.d1, 0, 1)

    @property
    def d_n_d2(self) -> float:
        return norm.pdf(self.d2, 0, 1)

    ##################################################### VANILLA ######################################################
    @property
    def price_call_bs(self) -> float:
        """
        :return: the price of a call with the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        t = self._maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        n_d2 = self.n_d2
        return s * n_d1 * np.exp(-q * t / b) - k * np.exp(-r * t / b) * n_d2

    @property
    def price_put_bs(self) -> float:
        """
        :return: the price of a put with the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        t = self._maturity
        b = self.__annual_basis
        n_md1 = 1 - self.n_d1
        n_md2 = 1 - self.n_d2
        return k * n_md2 * np.exp(-r * t / b) - s * n_md1 * np.exp(-q * t / b)

    @property
    def delta_call_bs(self) -> float:
        """
        :return: the delta of a call with the BS model
        """
        q = self._dividend
        t = self._maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        return np.exp(-q * t / b) * n_d1

    @property
    def delta_put_bs(self) -> float:
        """
        :return: the delta of a put with the BS model
        """
        q = self._dividend
        t = self._maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        return np.exp(-q * t / b) * (n_d1 - 1)

    @property
    def theta_call_bs(self) -> float:
        """
        :return: the theta of a call with the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        sig = self._volatility
        t = self._maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        n_d2 = self.n_d2
        d_n_d1 = self.d_n_d1
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) + q * np.exp(-q * t / b) * s * n_d1
                - r * np.exp(-r * t / b) * k * n_d2) / b

    @property
    def theta_put_bs(self) -> float:
        """
        :return: the theta of a put with the BS model
        """
        s = self._spot
        k = self.__strike
        r = self._rate
        q = self._dividend
        sig = self._volatility
        t = self._maturity
        b = self.__annual_basis
        n_md1 = 1 - self.n_d1
        n_md2 = 1 - self.n_d1
        d_n_d1 = self.d_n_d1
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) - q * np.exp(-q * t / b) * s * n_md1
                + r * np.exp(-r * t * b) * k * n_md2) / b

    @property
    def gamma_bs(self) -> float:
        """
        :return: the gamma with the BS model
        """
        s = self._spot
        q = self._dividend
        sig = self._volatility
        t = self._maturity
        b = self.__annual_basis
        d_n_d1 = self.d_n_d1
        return (np.exp(-q * t / b) / (s * sig * np.sqrt(t / b))) * d_n_d1

    @property
    def vega_bs(self) -> float:
        """
        :return: the vega with the BS model
        """
        s = self._spot
        q = self._dividend
        t = self._maturity
        b = self.__annual_basis
        d_n_d1 = self.d_n_d1
        return (np.exp(-q * t / b) * s * np.sqrt(t / b) * d_n_d1) / 100

    @property
    def rho_call_bs(self) -> float:
        """
        :return: the rho of a call with the BS model
        """
        t = self._maturity
        k = self.__strike
        r = self._rate
        b = self.__annual_basis
        n_d2 = self.n_d2
        return ((t / b) * k * np.exp(-r * t / b) * n_d2) / 100

    @property
    def rho_put_bs(self) -> float:
        """
        :return: the rho of a put with the BS model
        """
        t = self._maturity
        k = self.__strike
        r = self._rate
        b = self.__annual_basis
        n_d2 = self.n_d2
        return ((t / b) * k * np.exp(-r * t / b) * n_d2 - (t / b) * k * np.exp(-r * t / b)) / 100

    ##################################################### BINARY #######################################################
    def price_call_digital_bs(self, payoff) -> float:
        """
        :return: the price of a digital call with the BS model (Bull digital)
        """
        p = payoff
        r = self.rate
        t = self.maturity
        b = self.annual_basis
        n_d2 = self.n_d2
        return p * np.exp(-r * t / b) * n_d2

    def price_put_digital_bs(self, payoff) -> float:
        """
        :return: the price of a digital put with the BS model (Bear digital)
        """
        p = payoff
        r = self._rate
        t = self._maturity
        b = self.__annual_basis
        n_md2 = 1 - self.n_d2
        return p * np.exp(-r * t / b) * n_md2 #ATTENTION correction skew*vega

    @property
    def delta_digital_call_bs(self) -> float:
        """
        :return: the delta of a digital call with the BS model
        """
        s = self.spot
        r = self.rate
        t = self.maturity
        sig = self._volatility
        b = self.annual_basis
        d_n_d2 = self.d_n_d2
        return (np.exp(-r * t / b) * d_n_d2)/(sig * s * np.sqrt(t / b)) #ATTENTION correction skew*vega

    @property
    def gamma_digital_call_bs(self) -> float:
        """
        :return: the delta of a digital call with the BS model
        """
        s = self.spot
        r = self.rate
        t = self.maturity
        sig = self._volatility
        b = self.annual_basis
        d1 =  self.d1
        d_n_d2 = self.d_n_d2
        return (np.exp(-r * t / b) * d_n_d2)/(sig * s * np.sqrt(t / b)) #ATTENTION correction skew*vega

