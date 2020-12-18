import numpy as np


class Returns:

    def __init__(self, returns, freq=250, replace_nan=True):
        if replace_nan:
            returns = [0 if np.isnan(x) else x for x in returns]
        self.__returns = returns
        self.__freq = freq

    def get_cumulative_returns(self):
        return list(np.cumprod([x + 1 for x in self.__returns]) - 1)

    def signals_to_returns(self, signals):
        if len(signals) != len(self.__returns):
            raise ValueError('Signals must be the same length as returns')
        signal_returns = [x * y for x, y in zip(self.__returns, signals)]
        return Returns(signal_returns, self.__freq)

    def get_freq(self):
        return self.__freq

    def get_returns(self):
        return self.__returns

    def __len__(self):
        return len(self.__returns)

    def __str__(self):
        return f'{self.__returns}'
