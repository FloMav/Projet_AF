import numpy as np
import scipy.stats as ss
from scipy.stats import norm
from scipy.stats import multivariate_normal
from functions.probabilities import Heston_pdf, Q1, Q2

class Heston:
    def __init__(self,
                 spot: float,
                 strike: float,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 volatility: float,
                 volatility_vol: float = 0.3,
                 mu: float = 0.1,
                 kappa: float = 2,
                 theta: float = 0.04,
                 rho: float = -0.2,
                 annual_basis: int = 365,
                 steps: int = 2,
                 paths: int = 5,
                 u: float = 0.0001,
                 limit_max = 1000):
        """
        :param spot: spot price
        :param strike: strike price
        :param rate: risk free rate 0.05 corresponds to 5%
        :param dividend: dividend yield 0.01 corresponds to 1%
        :param maturity: maturity in days
        :param volatility: volatility 0.16 corresponds to 16%
        :param volatility_vol: volatility of volatility
        :param mu: drift of the stock process
        :param kappa: mean reversion coeff of the variance process, ATTENTION CONDITION FELLER 2*kappa*theta > sigma^2
        :param theta: long term mean of the variance process
        :param rho:  correlation between W1 and W2, <W1,W2>
        :param steps:  number of steps
        :param paths:  number of paths
        :param u:  number of ??
        :param limit_max:  number of ??
        """
        self.__spot = spot
        self.__strike = strike
        self.__rate = rate
        self.__dividend = dividend
        self.__maturity = maturity
        self._volatility = volatility
        self._volatility_vol = volatility_vol
        self.__mu = mu
        self.__kappa = kappa
        self.__theta = theta
        self.__rho = rho
        self.__annual_basis = annual_basis
        self.__steps = steps
        self.__paths = paths
        self.__u = u
        self.__limit_max = limit_max

        assert 2*kappa*theta > volatility**2, 'Feller condition not verified : 2*kappa*theta > volatility^2'

    @property
    def spot(self) -> float:
        return self.__spot

    @property
    def strike(self) -> float:
        return self.__strike

    @property
    def rate(self) -> float:
        return self.__rate

    @property
    def dividend(self) -> float:
        return self.__dividend

    @property
    def maturity(self) -> int:
        return self.__maturity

    @property
    def volatility(self) -> float:
        return self._volatility

    @property
    def volatility_vol(self) -> float:
        return self._volatility_vol

    @property
    def mu(self) -> float:
        return self.__mu

    @property
    def kappa(self) -> float:
        return self.__kappa

    @property
    def theta(self) -> float:
        return self.__theta

    @property
    def rho(self) -> float:
        return self.__rho

    @property
    def annual_basis(self) -> float:
        return self.__annual_basis

    @property
    def steps(self) -> int:
        return self.__steps

    @property
    def paths(self) -> int:
        return self.__paths

    @property
    def u(self) -> float:
        return self.__u

    @property
    def limit_max(self) -> int:
        return self.__limit_max

    ################################################### MONTE CARLO ####################################################

    @property
    def mc_paths(self) -> np.matrix:
        MU = np.array([0, 0])
        COV = np.matrix([[1, self.rho], [self.rho, 1]])
        W = multivariate_normal.rvs(mean=MU, cov=COV, size=(self.paths, self.steps-1))

        W_S = W[:, 0]
        W_v = W[:, 1]

        S = np.zeros((self.paths, self.steps))
        S[:, 0] = np.log(self.spot)

        V = np.zeros((self.paths, self.steps))
        V[:, 0] = np.log(self.volatility)

        v = np.zeros(self.steps)

        maturity_vec, dt = np.linspace(0, self.maturity, self.steps, retstep=True)

        for t in range(0, N - 1):
            v = np.exp(V[:, t])
            v_sq = np.sqrt(v)
            dt_sq = np.qrt(dt)

            V[:, t + 1] = V[:, t] + (1 / v) * (self.kappa * (self.theta - v) - 0.5 * self.volatility_vol ** 2) * dt + self.volatility_vol * (1 / v_sq) * dt_sq * W_v[:, t]
            #may be take np.base discretization CIR
            #when is it used ??
            S[:, t + 1] = S[:, t] + (self.mu - 0.5 * v) * dt + v_sq * dt_sq * W_S[:, t]

            #or do we use Cython???

            DiscountedPayoff = np.exp(-self.rate * self.maturity) * np.maximum(S - self.strike, 0)
            V = scp.mean(DiscountedPayoff)


        return V

    ############################################ CHARACTERISTIC FUNCTION ###############################################

    def characteristic_function(self):
        xi = self.kappa - self.volatility_vol * self.rho * u * 1j
        d = np.sqrt(xi ** 2 + self.volatility_vol ** 2 * (u ** 2 + 1j * u))
        g1 = (xi + d) / (xi - d)
        cf = np.exp(1j * u * self.mu * t + (self.kappa * self.theta) / (self.volatility_vol ** 2) * (\
                (xi + d) * t - 2 * np.log((1 - g1 * np.exp(d * t)) / (1 - g1))) \
                    + (self.volatility / self.volatility_vol ** 2) * (xi + d) * (1 - np.exp(d * t)) / (1 - g1 * np.exp(d * t)))
        call = self.spot * Q1(self.strike, cf, limit_max) - self.strike * np.exp(-self.rate * self.maturity) * Q2(self.strike, cf, limit_max)
        #value for a put??? Q(-...)???
        # pb w/ installing functions.probabilities (Q1, Q2)
        return cf

    def characteristic_function_2(self):
        xi = self.kappa - self.volatility_vol * self.rho * u * 1j
        d = np.sqrt(xi ** 2 + self.volatility_vol ** 2 * (u ** 2 + 1j * u))
        g1 = (xi + d) / (xi - d)
        g2 = 1 / g1
        cf = np.exp(1j * u * self.mu * t + (self.kappa * self.theta) / (self.volatility_vol ** 2) * (\
                    (xi - d) * t - 2 * np.log((1 - g2 * np.exp(-d * t)) / (1 - g2))) \
                    + (self.volatility / self.volatility_vol ** 2) * (xi - d) * (1 - np.exp(-d * t)) / (1 - g2 * np.exp(-d * t)))
        call = self.spot * Q1(self.strike, cf, limit_max) - self.strike * np.exp(-self.rate * self.maturity) * Q2(self.strike, cf, limit_max)
        # value for a put??? Q(-...)???
        #pb w/ installing functions.probabilities (Q1, Q2)
        return call
