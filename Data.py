import json
import requests
import pandas as pd
from tqdm import tqdm
import datetime
import certifi
import urllib.request
import numpy as np

class Data:
    def __init__(self):
        pass

    @property
    def imported_data(self):
        return self.importation()

    @property
    def df_smile(self):
        return Data.maturity_sel(Data.data_preprocessing(), 5)

    @staticmethod
    def importation():
        df = pd.read_csv("Data/data_test_1.csv", sep=";", index_col=0)
        #df = df.rename(columns={"Close": "Spot"})
        return df

    @staticmethod
    def get_option_name_and_settlement(coin='BTC'):
        """
        :param coin: crypto-currency coin name ('BTC', ...)
        :return: 2 lists:
                            1.  list of traded options for the selected coin;
                            2.  list of settlement period for the selected coin.
        """

        # requests public API
        r = requests.get("https://test.deribit.com/api/v2/public/get_instruments?currency=" + coin + "&kind=option")
        result = json.loads(r.text)

        # get option name
        name = pd.json_normalize(result['result'])['instrument_name']
        name = list(name)

        # get option settlement period
        settlement_period = pd.json_normalize(result['result'])['settlement_period']
        settlement_period = list(settlement_period)

        return name, settlement_period

    @staticmethod
    def get_option_data(coin='BTC'):
        """
        :param coin: crypto-currency coin name ('BTC', ...)
        :return: pandas data frame with all option data for a given coin
        """

        # get option name and settlement
        coin_name = Data.get_option_name_and_settlement(coin)[0]
        settlement_period = Data.get_option_name_and_settlement(coin)[1]

        # initialize data frame
        coin_df = []

        # initialize progress bar
        pbar = tqdm(total=len(coin_name))

        # loop to download data for each Option Name
        for i in range(len(coin_name)):
            # download option data -- requests and convert json to pandas
            r = requests.get('https://test.deribit.com/api/v2/public/get_order_book?instrument_name=' + coin_name[i])
            result = json.loads(r.text)
            df = pd.json_normalize(result['result'])

            # add settlement period
            df['settlement_period'] = settlement_period[i]

            # append data to data frame
            coin_df.append(df)

            # update progress bar
            pbar.update(1)

        # finalize data frame
        coin_df = pd.concat(coin_df)

        # remove useless columns from coin_df
        columns = ['state', 'estimated_delivery_price']
        coin_df.drop(columns, inplace=True, axis=1)

        # close the progress bar
        pbar.close()
        return coin_df

    @staticmethod
    def get_all_active_options(coin='BTC'):
        """
        :param coin: 'BTC' or ...
        :return: list of all active options from the Deribit API
        """

        # url connection
        url = "https://test.deribit.com/api/v2/public/get_instruments?currency=" + coin + "&kind=option&expired=false"
        with urllib.request.urlopen(url, cafile=certifi.where()) as url:
            data = json.loads(url.read().decode())
        data = pd.DataFrame(data['result']).set_index('instrument_name')
        data['creation_date'] = pd.to_datetime(data['creation_timestamp'], unit='ms')
        data['expiration_date'] = pd.to_datetime(data['expiration_timestamp'], unit='ms')

        print(f'{data.shape[0]} active options')

        return data

    @staticmethod
    def filter_options(price, active_options):
        """
        :param price: current coin price
        :param active_options: list of active options
        :return: list of active options after filtration
        """

        # Get Put/Call information
        pc = active_options.index.str.strip().str[-1]

        # Set "moneyness"
        active_options['m'] = active_options['strike'] / price
        active_options.loc[pc == 'P', 'm'] = -active_options['m']

        # Set days until expiration
        active_options['t'] = (active_options['expiration_date'] - pd.Timestamp.today()).dt.days

        return active_options

    @staticmethod
    def get_tick_data(instrument_name):     # Get Tick data for a given instrument from the Deribit API
        # url connection
        url = f"https://test.deribit.com/api/v2/public/ticker?instrument_name={instrument_name}"
        with urllib.request.urlopen(url, cafile=certifi.where()) as url:
            data = json.loads(url.read().decode())

        # convert json to pandas.DataFrame
        data = pd.json_normalize(data['result'])
        data.index = [instrument_name]

        return data

    @staticmethod
    def get_all_option_data(coin): # Loop through all filtered options to get the current 'ticker' data
        # get tick data Perpetual
        option_data = Data.get_tick_data(coin + '-PERPETUAL')

        # get active options
        options = Data.filter_options(price=option_data['last_price'][0], active_options=Data.get_all_active_options(coin=coin))
        for o in options.index:
            option_data = option_data.append(Data.get_tick_data(o))

        return option_data

    @staticmethod
    def data_preprocessing(coin='BTC'): # data pre-processing
        """
        :param coin: 'BTC' or 'ETH'
        :return: pandas.DataFrame with relevant financial data
        """

        # disable false positive warning, default='None'
        pd.options.mode.chained_assignment = None

        # get data
        print('Get ' + coin + ' options data')
        df = Data.get_all_option_data(coin=coin)

        # add additional metrics to data
        df['t'] = np.nan
        df['strike'] = np.nan
        df['expiration'] = np.nan

        # indexing index
        index = df[1:].index.map(lambda x: x.split('-'))

        # calculate days until expiration
        days = [element[1] for element in index]
        maturity = days
        days = (pd.to_datetime(days) - pd.Timestamp.today()).days

        # add days to expiration
        df.t[1:] = np.array(days)

        # Pull strike from instrument name
        strike = [int(element[2]) for element in index]

        # add strike
        df.strike[1:] = strike

        # calculate moneyness
        df['m'] = df['strike'] / df['last_price'][0]

        # pull maturity
        maturity = pd.to_datetime(maturity) + pd.DateOffset(hours=10)
        maturity = maturity.astype('int64')
        df.expiration[1:] = maturity

        # consider only t>0
        df = df.query('t>0')

        print('additional metrics added')
        print('----------------------------------------------------------------------')

        return df

    @staticmethod
    def maturity_sel(coin_df, time_to_maturity, coin='BTC'): #  select for maturity
        # subset df
        call_df = coin_df[coin_df['instrument_name'].str.contains('-C')]

        # pull days to maturity
        days_to_maturity = list(call_df['t'].unique())
        maturity = min(days_to_maturity, key=lambda x: abs(x - time_to_maturity))

        # subset df for the maturity
        df = call_df[call_df['t'] == maturity].sort_values('m')

        return df



