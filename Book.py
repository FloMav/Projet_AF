import pandas as pd
from BinaryOption import BinaryOption


class Book:
    """

    """
    def __init__(self,
                 data,
                 opt,
                 pricing_method='BS'):
        """

        :param data:
        :param opt:
        :param pricing_method:
        """
        self.__data: pd.DataFrame = data
        self.__opt: dict = opt
        self.__pricing_method = pricing_method

    @property
    def book(self):
        book = dict()
        for opt in self.__opt:
            book[opt] = BinaryOption(self.__data.iloc[0, self.__data.columns.get_loc('Spot')],
                                        self.__opt[opt]['Strike'],
                                        self.__data.iloc[0, self.__data.columns.get_loc('Interest Rate')],
                                        self.__data.iloc[0, self.__data.columns.get_loc('Dividend Yield')],
                                        self.__opt[opt]['Maturity'],
                                        self.__data.iloc[0, self.__data.columns.get_loc('Volatility')],
                                        payoff=self.__opt[0, self.__data.columns.get_loc('Payoff')],
                                        typ=self.__opt[opt]['Type'],
                                        pricing_method=self.__pricing_method)
        return book

    @property
    def delta_book(self):
        delta_book = dict()
        for opt in self.__opt:
            delta_book[opt] = self.book[opt].record['Delta_spread']

    def gamma_book(self):

    def theta_book(self):

    def vega_book(self):

    def rho_book(self):

    def report(self):
        for date in self.book:
            columns = ['Type', 'Position', 'Payoff', 'Spot', 'Strike', 'Interest Rate (%)', 'Dividend Yield (%)',
                           'Implied Volatility (%)', 'Maturity T (minuts)']
            index = [f"Opt {i+1}" for i in range(len(self.book[date]))]
            df = pd.DataFrame(columns=columns, index=index)
            for i in range(len(self.book[date])):
                df.loc[f"Opt {i+1}", 'Type'] = self.book[date][i].typ
                df.loc[f"Opt {i + 1}", 'Position'] = 0
                df.loc[f"Opt {i + 1}", 'Payoff'] = self.book[date][i].payoff
                df.loc[f"Opt {i + 1}", 'Spot'] = self.book[date][i].spot
                df.loc[f"Opt {i + 1}", 'Strike'] = self.book[date][i].strike
                df.loc[f"Opt {i + 1}", 'Interest Rate (%)'] = self.book[date][i].rate
                df.loc[f"Opt {i + 1}", 'Dividend Yield (%)'] = self.book[date][i].dividend
                df.loc[f"Opt {i + 1}", 'Implied Volatility (%)'] = self.book[date][i].volatility
                df.loc[f"Opt {i + 1}", 'Maturity T (minuts)'] = self.book[date][i].maturity

            df.to_csv(f'Report/{date}.csv')
        pass

    def backtest(self):
        print(self.__data.columns)
        for date in self.__data.index():
            tup = tuple(self.__data.loc[date])
            for opt in self.__opt:
                print(tup)
                #self.__opt[opt].setter(tup)


