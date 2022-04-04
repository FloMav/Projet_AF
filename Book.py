import pandas as pd
import datetime as dt
from BinaryOption import BinaryOption


class Book:
    """

    """
    def __init__(self, data, opt):
        self.__data: pd.DataFrame = data
        self.__opt: dict = opt

    @property
    def book(self):
        book = dict()
        for date in self.__data.index:
            book[date] = list()
            for opt in self.__opt:
                maturity = (dt.datetime.strptime(self.__opt[opt]['Maturity'], '%Y-%m-%d %H:%M:%S') -
                            dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
                maturity = int(maturity.total_seconds()/60) ### ATTENTION A LA FREQUENCE
                if maturity >= 0:
                    book[date].append(BinaryOption(self.__data.loc[date, 'Spot'],
                                                   self.__opt[opt]['Strike'],
                                                   self.__data.loc[date, 'Interest Rate'],
                                                   self.__data.loc[date, 'Dividend Yield'],
                                                   maturity,
                                                   self.__data.loc[date, 'Volatility'],
                                                   typ=self.__opt[opt]['Type'],
                                                   payoff=self.__opt[opt]['Payoff']))

        return book

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


