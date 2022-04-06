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

# import json
# import requests
# import pandas as pd
# from tqdm import tqdm
# import sqlite3
# import datetime
# import certifi
#
# # functions
# def get_option_name_and_settlement(coin='BTC'):
#     """
#     :param coin: crypto-currency coin name ('BTC', ...)
#     :return: 2 lists:
#                         1.  list of traded options for the selected coin;
#                         2.  list of settlement period for the selected coin.
#     """
#
#     # requests public API
#     r = requests.get("https://test.deribit.com/api/v2/public/get_instruments?currency=" + coin + "&kind=option")
#     result = json.loads(r.text)
#
#     # get option name
#     name = pd.json_normalize(result['result'])['instrument_name']
#     name = list(name)
#
#     # get option settlement period
#     settlement_period = pd.json_normalize(result['result'])['settlement_period']
#     settlement_period = list(settlement_period)
#
#     return name, settlement_period
#
#
# def get_option_data(coin='BTC'):
#     """
#     :param coin: crypto-currency coin name ('BTC', ...)
#     :return: pandas data frame with all option data for a given coin
#     """
#
#     # get option name and settlement
#     coin_name = get_option_name_and_settlement(coin)[0]
#     settlement_period = get_option_name_and_settlement(coin)[1]
#
#     # initialize data frame
#     coin_df = []
#
#     # initialize progress bar
#     pbar = tqdm(total=len(coin_name))
#
#     # loop to download data for each Option Name
#     for i in range(len(coin_name)):
#         # download option data -- requests and convert json to pandas
#         r = requests.get('https://test.deribit.com/api/v2/public/get_order_book?instrument_name=' + coin_name[i])
#         result = json.loads(r.text)
#         df = pd.json_normalize(result['result'])
#
#         # add settlement period
#         df['settlement_period'] = settlement_period[i]
#
#         # append data to data frame
#         coin_df.append(df)
#
#         # update progress bar
#         pbar.update(1)
#
#     # finalize data frame
#     coin_df = pd.concat(coin_df)
#
#     # remove useless columns from coin_df
#     columns = ['state', 'estimated_delivery_price']
#     coin_df.drop(columns, inplace=True, axis=1)
#
#     # close the progress bar
#     pbar.close()
#
#     return coin_df
#
#
#
