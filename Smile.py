import pandas as pd
import pysabr
import matplotlib.pyplot as plt
import numpy as np
from pysabr import Hagan2002LognormalSABR as LNsabr
from pysabr import hagan_2002_lognormal_sabr as hagan2002LN


class Smile:
    def __init__(self):
        pass

    strikes = test_10.strike
    LogNormalVols = test_10.mark_iv

    spot = 45319.10

    beta = 0.5
    calibration_LN = LNsabr(f=spot, shift=0, t=5, beta=beta).fit(strikes, LogNormalVols)
    modelVols_LN = []
    test_LN = []

    for strike in strikes:
        test_LN.append(hagan2002LN.lognormal_vol(strike, f=spot, t=5, alpha=calibration_LN[0], beta=beta,
                                                 rho=calibration_LN[1], volvol=calibration_LN[2]) * 100.00)

    print(calibration_LN)
    print(test_LN)



    def optimisation_sabr(spot: float,
                          strikes: list,
                          implied_vol: list,
                          t: float,
                          shift: float = 0,
                          beta: float = 0.5) -> list:
        import pysabr
        import numpy as np
        from pysabr import Hagan2002LognormalSABR as LNsabr
        from pysabr import hagan_2002_lognormal_sabr as hagan2002LN

        calibration_LN = LNsabr(f=spot, shift=shift, t=t, beta=beta).fit(strikes, implied_vol)

        return calibration_LN


    param=optimisation_sabr(45319.10,test_10.strike,test_10.mark_iv,5)
    param

    def vol_pred_sabr(strike: float,
                      spot: float,
                      calibration_LN: list,
                      t: float,
                      beta: float = 0.5) -> float:
        log_vol = hagan2002LN.lognormal_vol(strike, f=spot, t=t, alpha=calibration_LN[0], beta=beta,
                                            rho=calibration_LN[1], volvol=calibration_LN[2]) * 100.00

        return log_vol

    vol_pred_sabr(44000, 45319.10, param, 10)

    plt.plot(strikes, np.array(test_10.mark_iv), "r--", strikes, test_LN)

    strikes