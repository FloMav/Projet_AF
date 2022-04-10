import numpy as np
import pandas as pd
from BinaryOption import BinaryOption

class Book:
    """

    """
    def __init__(self,
                 data,
                 opt,
                 initial_cash: float = 1000000,
                 pricing_method='BS'):
        """

        :param data:
        :param opt:
        :param pricing_method:
        """
        self.__data: pd.DataFrame = data
        self.__opt: dict = opt
        self.__pricing_method: str = pricing_method
        self.__initial_cash_digital = initial_cash
        self.__initial_cash_spread = initial_cash
        self.__previous_date = 0
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
                                     smile_active=False)
        self.__book: dict = dico

    @property
    def book_objets(self) -> dict[int]:
        return self.__book

    @property
    def book_positions(self) -> dict[str]: #dictionnaire de Df qui montre l'impact des options dans le book at t avec index = options, cle du dictionnaire = t
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
                if date in self.__book[opt].record.index:
                    df.loc[len(df)+1] = self.__book[opt].record.loc[date].values
                    idx = list(df.index)
                    idx[-1] = opt
                    df.index = idx
            df.insert(8, 'Weight_digital', df["Price_digital"] / df["Price_digital"].sum() * 100)
            df.insert(10, 'Weight_spread', df["Price_spread"] / df["Price_spread"].sum() * 100)

            digtal_portfolio_value = df["Price_digital"].sum()
            digtal_portfolio_weight = df["Weight_digital"].sum()
            spread_portfolio_value = df["Price_spread"].sum()
            spread_portfolio_weight = df["Weight_spread"].sum()
            digital_portfolio_delta = (df["Delta_digital"] * df["Price_digital"]).sum() / digtal_portfolio_value
            spread_portfolio_delta = (df["Delta_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
            digital_portfolio_gamma = (df["Gamma_digital"] * df["Price_digital"]).sum() / digtal_portfolio_value
            spread_portfolio_gamma = (df["Gamma_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
            digital_portfolio_vega = (df["Vega_digital"] * df["Price_digital"]).sum() / digtal_portfolio_value
            spread_portfolio_vega = (df["Vega_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
            digital_portfolio_theta = (df["Theta_digital"] * df["Price_digital"]).sum() / digtal_portfolio_value
            spread_portfolio_theta = (df["Theta_spread"] * df["Price_spread"]).sum() / spread_portfolio_value
            digital_portfolio_rho = (df["Rho_digital"] * df["Price_digital"]).sum() / digtal_portfolio_value
            spread_portfolio_rho = (df["Rho_spread"] * df["Price_spread"]).sum() / spread_portfolio_value

            df.loc["Options"] = [" ",
                                    df['Spot'].iloc[0],
                                    np.NAN,  #Strike
                                    df['Rate'].iloc[0],  #Rate
                                    df['Dividend'].iloc[0],  #Dividend
                                    np.NAN,  #Maturity
                                    np.NAN,  #Volatility
                                   digtal_portfolio_value,
                                   digtal_portfolio_weight,
                                   spread_portfolio_value,
                                   spread_portfolio_weight,
                                   digital_portfolio_delta,
                                   spread_portfolio_delta,
                                   digital_portfolio_gamma,
                                   spread_portfolio_gamma,
                                   digital_portfolio_vega,
                                   spread_portfolio_vega,
                                   digital_portfolio_theta,
                                   spread_portfolio_theta,
                                   digital_portfolio_rho,
                                   spread_portfolio_rho,
                                   ]

            dico[date] = df
        return dico

    @property
    def book_track(self): # Df qui montre l'evolution du book sur chaque periode index = date
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
            # digital_portfolio_delta_und = digital_portfolio_delta * digtal_portfolio_value / (
            #             digtal_portfolio_value + und_digital)
            # spread_portfolio_delta_und = spread_portfolio_delta * spread_portfolio_value / (
            #             spread_portfolio_value + und_spread)
            # digital_portfolio_gamma_und = digital_portfolio_delta * digtal_portfolio_value / (
            #             digtal_portfolio_value + und_digital)
            # spread_portfolio_gamma_und = spread_portfolio_delta * spread_portfolio_value / (
            #             spread_portfolio_value + und_spread)
            # digital_portfolio_vega_und = digital_portfolio_delta * digtal_portfolio_value / (
            #             digtal_portfolio_value + und_digital)
            # spread_portfolio_vega_und = spread_portfolio_delta * spread_portfolio_value / (
            #             spread_portfolio_value + und_spread)
            # digital_portfolio_theta_und = digital_portfolio_delta * digtal_portfolio_value / (
            #             digtal_portfolio_value + und_digital)
            # spread_portfolio_theta_und = spread_portfolio_delta * spread_portfolio_value / (
            #             spread_portfolio_value + und_spread)
            # digital_portfolio_rho_und = digital_portfolio_delta * digtal_portfolio_value / (
            #             digtal_portfolio_value + und_digital)
            # spread_portfolio_rho_und = spread_portfolio_delta * spread_portfolio_value / (
            #             spread_portfolio_value + und_spread)

            if date == self.__data.index[0]:
                cash_digital = self.__initial_cash_digital
                cash_spread = self.__initial_cash_spread
            else:
                cash_digital = df.loc[(self.__previous_date, "Delta_hedge"), 'Price_digital']
                cash_spread = df.loc[(self.__previous_date, "Delta_hedge"), 'Price_spread']

            df.loc[(date, "Options")] = self.book_positions[date].loc['Options']
            df.loc[(date, "Delta_hedge")] = [df.loc[(date, "Options"), 'Spot'],
                                               np.NAN,
                                               df.loc[(date, "Options"), 'Rate'],
                                               df.loc[(date, "Options"), 'Dividend'],
                                               np.NAN,
                                               np.NAN,
                                               df.loc[(date, "Options"), 'Spot'] * (-df.loc[(date, "Options"), 'Delta_digital']),
                                               df.loc[(date, "Options"), 'Spot'] * (-df.loc[(date, "Options"), 'Delta_spread']),
                                               - df.loc[(date, "Options"), 'Delta_digital'],
                                               - df.loc[(date, "Options"), 'Delta_spread'],
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0]
            df.loc[(date, "Cash")] = [df.loc[(date, "Options"), 'Spot'],
                                               np.NAN,
                                               df.loc[(date, "Options"), 'Rate'],
                                               df.loc[(date, "Options"), 'Dividend'],
                                               np.NAN,
                                               np.NAN,
                                               cash_digital - df.loc[(date, "Options"), 'Price_digital'] + df.loc[(date, "Delta_hedge"), 'Price_digital'],
                                               cash_spread - df.loc[(date, "Options"), 'Price_spread'] + df.loc[(date, "Delta_hedge"), 'Price_spread'],
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
            df.loc[(date, "Portfolio")] = [df.loc[(date, "Options"), 'Spot'],
                                               np.NAN,
                                               df.loc[(date, "Options"), 'Rate'],
                                               df.loc[(date, "Options"), 'Dividend'],
                                               np.NAN,
                                               np.NAN,
                                               df.loc[(date, "Options"), 'Price_digital'] - df.loc[(date, "Delta_hedge"), 'Price_digital'] + df.loc[(date, "Cash"), 'Price_digital'],
                                               0, #df.loc[(date, "Options"), 'Spot'] * (-df.loc[(date, "Options"), 'Delta_spread']),
                                               df.loc[(date, "Options"), 'Delta_digital'] + df.loc[(date, "Delta_hedge"), 'Delta_digital'] + df.loc[(date, "Cash"), 'Delta_digital'],
                                               df.loc[(date, "Options"), 'Delta_spread'] + df.loc[(date, "Delta_hedge"), 'Delta_spread'] + df.loc[(date, "Cash"), 'Delta_spread'],
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0]
            self.__previous_date = date
        df.drop(['Strike', 'Rate', 'Dividend', 'Maturity', 'Volatility'], axis=1, inplace=True)
        return df


    def backtest(self) -> None: # ATTENTION A NE PAS LE RUN 2 TIMES IN A ROW
        for opt in self.__opt:
            for date in self.__data.index[1:]:
                tup = self.__data.loc[date, :].values.tolist()
                tup = tuple(tup)
                self.__book[opt].setter(tup, date)
        print("\n\n############ Backtest done ! ############\n")
        return None