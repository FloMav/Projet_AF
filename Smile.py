
from pysabr import Hagan2002LognormalSABR as LNsabr
from pysabr import hagan_2002_lognormal_sabr as hagan2002LN
import Data


class Smile:
    def __init__(self, spot, maturity, date):
        self.__spot = spot
        self.__maturity = maturity
        self.__date = date
        self.__alpha = 0
        self.__beta = 0.5
        self.__rho = 0
        self.__volga = 0
        self.__shift = 0
        self.sabr_calibration()

    def volatility(self, strike):
        volatility = self.sabr(strike)
        return volatility

    def sabr(self, strike):
        log_vol = hagan2002LN.lognormal_vol(strike,
                                            f=self.__spot,
                                            t=self.__maturity,
                                            alpha=self.__alpha,
                                            beta=self.__beta,
                                            rho=self.__rho,
                                            volvol=self.__volga)
        return log_vol

    def sabr_calibration(self):
        df, maturity_best_fit = Data.Data().df_smile(self.__date, self.__maturity)
        calibration_LN = LNsabr(f=self.__spot, shift=self.__shift, t=maturity_best_fit, beta=self.__beta).fit(df.strike, df.mark_iv)
        self.__alpha = calibration_LN[0]
        self.__rho = calibration_LN[1]
        self.__volga = calibration_LN[2]
        pass
