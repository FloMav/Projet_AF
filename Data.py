import pandas as pd


class Data:
    def __init__(self):
        pass

    @property
    def imported_data(self):
        return self.importation()

    @staticmethod
    def importation():
        df = pd.read_csv("Data/data_test_1.csv", sep=";", index_col=0)
        #df = df.rename(columns={"Close": "Spot"})
        return df

    @staticmethod
    def df_smile(date, maturity):
        date = str(date[0]+date[1]+'_'+date[3]+date[4]+'_'+date[6]+date[7]+date[8]+date[9])
        df = pd.read_csv(f"Data/Smile/derebit_data_{date}.csv", sep=";", index_col=0)
        df = Data.maturity_sel(df, time_to_maturity=maturity)
        maturity_best_fit = df['t'].iloc[0]
        return df, maturity_best_fit

    @staticmethod
    def maturity_sel(df, time_to_maturity, coin='BTC'): #  select for maturity
        # subset df
        call_df = df[df['instrument_name'].str.contains('-C')]

        # pull days to maturity
        days_to_maturity = list(call_df['t'].unique())
        maturity = min(days_to_maturity, key=lambda x: abs(x - time_to_maturity))

        # subset df for the maturity
        df = call_df[call_df['t'] == maturity].sort_values('m')
        return df



