from Class.BinaryOption import BinaryOption
import numpy as np
import pandas as pd


class Book:
    """
        Compute the book of binary options
    """
    def __init__(self,
                 data,
                 opt,
                 initial_cash: float = 20000,
                 pricing_method: str = 'BS',
                 smile_active: bool = False,
                 delta_max: int = 1,
                 annual_basis: int = 365,
                 inception_date: str = "12/03/2022"):
        """
        :param data: dataframe containing all the input of the pricing
        :param opt: dictionnary of otpions
        :param pricing_method:
        :param smile_active:
        :param delta_max:
        :param annual_basis:
        """
        self.__data: pd.DataFrame = data
        self.__opt: dict = opt
        self.__pricing_method: str = pricing_method
        self.__initial_cash_digital: float = initial_cash
        self.__initial_cash_spread: float = initial_cash
        self.__previous_date = 0
        self.__smile_active: bool = smile_active
        self.__delta_max: int = delta_max
        self.__annual_basis: int = annual_basis

        dico = dict()
        for opt in self.__opt:
            dico[opt] = BinaryOption(self.__data.iloc[0, self.__data.columns.get_loc('Spot')],
                                     self.__opt[opt]['Strike'],
                                     self.__data.iloc[0, self.__data.columns.get_loc('Interest Rate')],
                                     self.__data.iloc[0, self.__data.columns.get_loc('Dividend Yield')],
                                     self.__opt[opt]['Maturity'],
                                     self.__data.iloc[0, self.__data.columns.get_loc('Volatility')],
                                     payoff=self.__opt[opt]['Payoff'],
                                     typ=self.__opt[opt]['Type'],
                                     pricing_method=self.__pricing_method,
                                     smile_active=self.__smile_active,
                                     delta_max=self.__delta_max,
                                     annual_basis=self.__annual_basis,
                                     inception_date=inception_date)
        self.__book: dict = dico

    @property
    def initial_cash(self) -> float:
        return self.__initial_cash_digital

    @property
    def book_objets(self) -> dict[int]:
        return self.__book

    @property
    def book_positions(self) -> dict[str]:
        """
        Dictionnary of Dataframe with the date as the key
        At the date t, the datframe has the different options as index
        """
        dico = dict()
        for date in self.__data.index:
            df = pd.DataFrame(columns=['Typ',
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

            for opt in self.__opt:
                if date in self.__book[opt].record.index.values:
                    df.loc[opt] = self.__book[opt].record.loc[date].values
                    if self.__opt[opt]['Position'] == 'Short':
                        df.loc[opt, 'Price_digital'] *= -1
                        df.loc[opt, 'Price_spread'] *= -1
                        df.loc[opt, 'Delta_digital'] *= -1
                        df.loc[opt, 'Delta_spread'] *= -1
                        df.loc[opt, 'Gamma_digital'] *= -1
                        df.loc[opt, 'Gamma_spread'] *= -1
                        df.loc[opt, 'Vega_digital'] *= -1
                        df.loc[opt, 'Vega_spread'] *= -1
                        df.loc[opt, 'Theta_digital'] *= -1
                        df.loc[opt, 'Theta_spread'] *= -1
                        df.loc[opt, 'Rho_digital'] *= -1
                        df.loc[opt, 'Rho_spread'] *= -1
                    idx = list(df.index)
                    idx[-1] = opt
                    df.index = idx

            if df.shape[0] != 0:
                list_pos = [self.__opt[option]['Position'] for option in df.index]
                df.insert(1, 'Position', list_pos)

                digtal_options_value = df["Price_digital"].sum()
                spread_options_value = df["Price_spread"].sum()
                digital_options_delta = (df["Delta_digital"] * df["Price_digital"]).sum() / digtal_options_value
                spread_options_delta = (df["Delta_spread"] * df["Price_spread"]).sum() / spread_options_value
                digital_options_gamma = (df["Gamma_digital"] * df["Price_digital"]).sum() / digtal_options_value
                spread_options_gamma = (df["Gamma_spread"] * df["Price_spread"]).sum() / spread_options_value
                digital_options_vega = (df["Vega_digital"] * df["Price_digital"]).sum() / digtal_options_value
                spread_options_vega = (df["Vega_spread"] * df["Price_spread"]).sum() / spread_options_value
                digital_options_theta = (df["Theta_digital"] * df["Price_digital"]).sum() / digtal_options_value
                spread_options_theta = (df["Theta_spread"] * df["Price_spread"]).sum() / spread_options_value
                digital_options_rho = (df["Rho_digital"] * df["Price_digital"]).sum() / digtal_options_value
                spread_options_rho = (df["Rho_spread"] * df["Price_spread"]).sum() / spread_options_value

                df.loc["Options"] = [" ",
                                        " ",
                                        df['Spot'].iloc[0],
                                        np.NAN,  #Strike
                                        df['Rate'].iloc[0],  #Rate
                                        df['Dividend'].iloc[0],  #Dividend
                                        np.NAN,  #Maturity
                                        np.NAN,  #Volatility
                                        digtal_options_value,
                                        spread_options_value,
                                        digital_options_delta,
                                        spread_options_delta,
                                        digital_options_gamma,
                                        spread_options_gamma,
                                        digital_options_vega,
                                        spread_options_vega,
                                        digital_options_theta,
                                        spread_options_theta,
                                        digital_options_rho,
                                        spread_options_rho,
                                        ]

            dico[date] = df
        return dico

    @property
    def book_delta_hedge(self) -> pd.DataFrame:
        """
        Dataframe with a multindex ([Dates], [Options, Delta_hedge, Cash, Portfolio])
        """
        df = pd.DataFrame(columns=['Spot',
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
                                   'Rho_spread'],
                          index=pd.MultiIndex.from_product(
                              [self.__data.index.values, ["Options", "Delta_hedge", "Cash", "Portfolio"]],
                              names=["Date", "Positions"]))

        for date in self.__data.index:
            try:
                df.loc[(date, "Options")] = self.book_positions[date].loc['Options']
            except KeyError:
                continue
            if df.shape[0] != 0:
                spot = df.loc[(date, "Options"), 'Spot']
                rate = df.loc[(date, "Options"), 'Rate']
                dividend = df.loc[(date, "Options"), 'Dividend']

                digital_delta_hedge_value = df.loc[(date, "Options"), 'Spot'] * (-df.loc[(date, "Options"), 'Delta_digital'])
                if np.isnan(digital_delta_hedge_value):
                    digital_delta_hedge_value = 0
                spread_delta_hedge_value = df.loc[(date, "Options"), 'Spot'] * (-df.loc[(date, "Options"), 'Delta_spread'])
                if np.isnan(spread_delta_hedge_value):
                    spread_delta_hedge_value = 0
                try:
                    digital_delta_hedge_delta = - df.loc[(date, "Options"), 'Delta_digital'] * df.loc[(date, "Options"), 'Price_digital'] / digital_delta_hedge_value
                except ZeroDivisionError:
                    digital_delta_hedge_delta = 0
                try:
                    spread_delta_hedge_delta = - df.loc[(date, "Options"), 'Delta_spread'] * df.loc[(date, "Options"), 'Price_spread'] / spread_delta_hedge_value
                except ZeroDivisionError:
                    spread_delta_hedge_delta = 0


                df.loc[(date, "Delta_hedge")] = [spot,
                                                np.NAN,
                                                rate,
                                                dividend,
                                                np.NAN,
                                                np.NAN,
                                                digital_delta_hedge_value,
                                                spread_delta_hedge_value,
                                                digital_delta_hedge_delta,
                                                spread_delta_hedge_delta,
                                                0,
                                                0,
                                                0,
                                                0,
                                                0,
                                                0,
                                                0,
                                                0]

                if date == self.__data.index[0]:
                    digital_cash_value = self.__initial_cash_digital
                    spread_cash_value = self.__initial_cash_spread
                    digital_cash_variation = - df.loc[(date, "Delta_hedge"), 'Price_digital'] - df.loc[(date, "Options"), 'Price_digital']
                    spread_cash_variation = - df.loc[(date, "Delta_hedge"), 'Price_spread'] - df.loc[(date, "Options"), 'Price_spread']
                    digital_cash_value += digital_cash_variation
                    spread_cash_value += spread_cash_variation
                else:
                    digital_cash_value = df.loc[(self.__previous_date, "Cash"), 'Price_digital']
                    spread_cash_value = df.loc[(self.__previous_date, "Cash"), 'Price_spread']
                    digital_cash_variation = - df.loc[(date, "Delta_hedge"), 'Price_digital'] + df.loc[(self.__previous_date, "Delta_hedge"), 'Price_digital']
                    spread_cash_variation = - df.loc[(date, "Delta_hedge"), 'Price_spread'] + df.loc[(self.__previous_date, "Delta_hedge"), 'Price_spread']
                    digital_cash_value += digital_cash_variation
                    spread_cash_value += spread_cash_variation

                df.loc[(date, "Cash")] = [spot,
                                            np.NAN,
                                            rate,
                                            dividend,
                                            np.NAN,
                                            np.NAN,
                                            digital_cash_value,
                                            spread_cash_value,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0]

                digital_portfolio_value = df.loc[(date, "Options"), 'Price_digital'] + df.loc[(date, "Delta_hedge"), 'Price_digital'] + df.loc[(date, "Cash"), 'Price_digital']
                spread_portfolio_value = df.loc[(date, "Options"), 'Price_spread'] + df.loc[(date, "Delta_hedge"), 'Price_spread'] + df.loc[(date, "Cash"), 'Price_spread']
                digital_portfolio_delta = (df["Delta_digital"] * df["Price_digital"]).sum() / digital_portfolio_value
                spread_portfolio_delta = (df["Delta_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
                digital_portfolio_gamma = (df["Gamma_digital"] * df["Price_digital"]).sum() / digital_portfolio_value
                spread_portfolio_gamma = (df["Gamma_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
                digital_portfolio_vega = (df["Vega_digital"] * df["Price_digital"]).sum() / digital_portfolio_value
                spread_portfolio_vega = (df["Vega_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
                digital_portfolio_theta = (df["Theta_digital"] * df["Price_digital"]).sum() / digital_portfolio_value
                spread_portfolio_theta = (df["Theta_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
                digital_portfolio_rho = (df["Rho_digital"] * df["Price_digital"]).sum() / digital_portfolio_value
                spread_portfolio_rho = (df["Rho_spread"] * df["Price_spread"]).sum() / spread_portfolio_value

                df.loc[(date, "Portfolio")] = [spot,
                                            np.NAN,
                                            rate,
                                            dividend,
                                            np.NAN,
                                            np.NAN,
                                            digital_portfolio_value,
                                            spread_portfolio_value,
                                            digital_portfolio_delta,
                                            spread_portfolio_delta,
                                            digital_portfolio_gamma,
                                            spread_portfolio_gamma,
                                            digital_portfolio_vega,
                                            spread_portfolio_vega,
                                           digital_portfolio_theta,
                                           spread_portfolio_theta,
                                           digital_portfolio_rho,
                                           spread_portfolio_rho
                                            ]
                self.__previous_date = date
        df.drop(['Strike', 'Rate', 'Dividend', 'Maturity', 'Volatility'], axis=1, inplace=True)
        return df


    def backtest(self) -> None: # ATTENTION A NE PAS LE RUN 2 TIMES IN A ROW
        for opt in self.__opt:
            stop = -1
            for date in self.__data.index[1:]:
                tup = self.__data.loc[date, :].values.tolist()
                tup = tuple(tup)
                if stop == 0:
                    continue
                else:
                    stop = self.__book[opt].setter(tup, date)
        print("\n\n############ Backtest done ! ############\n")
        return None

