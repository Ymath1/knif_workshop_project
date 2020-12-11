import pandas as pd

from beartype import beartype


class TimeSeries:

    @beartype
    def __init__(self, series: pd.Series):
        self.__series = series

    def calculate_returns(self):
        return self.__series.pct_change()

    def get_series(self):
        return self.__series

    def __len__(self):
        return len(self.__series)


class MovingAverage:

    def __init__(self, series: TimeSeries, window: int):
        self.__series = series
        self.__window = window
        self.__moving_average = self.__calculate_moving_average()

    def get_moving_average(self):
        return self.__moving_average

    def __calculate_moving_average(self):
        return self.__series.get_series().rolling(window=self.__window).mean()
