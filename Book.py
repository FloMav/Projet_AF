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
        self.__pricing_method: str = pricing_method
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
                                     pricing_method=self.__pricing_method)
        self.__book: dict = dico

    @property
    def book(self) -> dict:
        return self.__book

    def backtest(self) -> None:
        for opt in self.__opt:
            for date in self.__data.index[1:]:
                tup = self.__data.loc[date, :].values.tolist()
                tup.append(self.__opt[opt]['Maturity'])
                tup = tuple(tup)
                self.__book[opt].setter(tup)
        print("\n\n############ Backtest done ! ############\n")
        return None




    # def report(self):
    #     for date in self.book:
    #         columns = ['Type', 'Position', 'Payoff', 'Spot', 'Strike', 'Interest Rate (%)', 'Dividend Yield (%)',
    #                        'Implied Volatility (%)', 'Maturity T (minuts)']
    #         index = [f"Opt {i+1}" for i in range(len(self.book[date]))]
    #         df = pd.DataFrame(columns=columns, index=index)
    #         for i in range(len(self.book[date])):
    #             df.loc[f"Opt {i+1}", 'Type'] = self.book[date][i].typ
    #             df.loc[f"Opt {i + 1}", 'Position'] = 0
    #             df.loc[f"Opt {i + 1}", 'Payoff'] = self.book[date][i].payoff
    #             df.loc[f"Opt {i + 1}", 'Spot'] = self.book[date][i].spot
    #             df.loc[f"Opt {i + 1}", 'Strike'] = self.book[date][i].strike
    #             df.loc[f"Opt {i + 1}", 'Interest Rate (%)'] = self.book[date][i].rate
    #             df.loc[f"Opt {i + 1}", 'Dividend Yield (%)'] = self.book[date][i].dividend
    #             df.loc[f"Opt {i + 1}", 'Implied Volatility (%)'] = self.book[date][i].volatility
    #             df.loc[f"Opt {i + 1}", 'Maturity T (minuts)'] = self.book[date][i].maturity
    #
    #         df.to_csv(f'Report/{date}.csv')
    #     pass



