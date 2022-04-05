import pandas as pd


class Data:
    def __init__(self):
        pass

    @property
    def imported_data(self):
        return self.importation()

    @property
    def total_data(self):
        return self.total()

    @staticmethod
    def importation():
        df = pd.read_csv("Data/data_test_1.csv", sep=";", index_col=0)
        #df = df.rename(columns={"Close": "Spot"})
        return df

    def total(self):
        df = self.imported_data
        df['Interest Rate'] = [0 for i in self.imported_data.index]
        df['Volatility'] = [0 for i in self.imported_data.index]
        df['Dividend Yield'] = [0 for i in self.imported_data.index]
        return df
