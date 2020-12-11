import pandas as pd
import yfinance as yf

from beartype import beartype
from knif_workshop_project.modules.data_handling import TimeSeries


class YahooDataReader:

    @beartype
    def __init__(self, ticker: str):
        self.__ticker = ticker

    @beartype
    def download_historical_data(self, start_date: pd.Timestamp, end_date: pd.Timestamp):
        return yf.download(self.__ticker, start=start_date, end=end_date)

    def get_open_price(self, start_date: pd.Timestamp, end_date: pd.Timestamp):
        data = self.download_historical_data(start_date, end_date)
        return TimeSeries(data["Open"])

    def get_close_price(self, start_date: pd.Timestamp, end_date: pd.Timestamp):
        data = self.download_historical_data(start_date, end_date)
        return TimeSeries(data["Close"])


class TextDataReader:

    @beartype
    def __init__(self, path: str, *args, **kwargs):
        self.__data = self.__read_file(path, *args, **kwargs)
        self.__set_index()

    def __set_index(self):
        self.__data.set_index(pd.to_datetime(self.__data['Data']), drop=True, inplace=True)
        self.__data.drop('Data', axis=1, inplace=True)

    def get_open_price(self):
        return TimeSeries(self.__data["Otwarcie"])

    def get_close_price(self):
        return TimeSeries(self.__data["Zamkniecie"])

    @staticmethod
    @beartype
    def __read_file(path: str, *args, **kwargs):
        return pd.read_csv(path, *args, **kwargs)
