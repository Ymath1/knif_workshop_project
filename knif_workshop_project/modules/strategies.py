from beartype import beartype
from knif_workshop_project.modules.data_handling import TimeSeries, MovingAverage


class Strategy:

    def __init__(self):
        pass

    def generate_signal(self):
        raise NotImplementedError("Method must be overridden in the derived class!")

    def _is_valid(self):
        raise NotImplementedError("Method must be overridden in the derived class!")


class BuyHoldStrategy(Strategy):

    @beartype
    def __init__(self, series: TimeSeries):
        super().__init__()
        self.__series = series
        self._is_valid()

    def generate_signal(self):
        return 1

    def _is_valid(self):
        if len(self.__series) > 0:
            return True
        raise ValueError("Series has to contain any observation!")


class ReversalStrategy(Strategy):

    @beartype
    def __init__(self, series: TimeSeries):
        super().__init__()
        self.__series = series
        self._is_valid()

    def generate_signal(self):
        return -1 if self.__series.calculate_returns()[-1] > 0 else 1

    def _is_valid(self):
        if len(self.__series) > 0:
            return True
        raise ValueError("Series has to contain any observation!")


class MovingAverageCrossoverStrategy(Strategy):

    @beartype
    def __init__(self, series: TimeSeries, short_ma_window: int, long_ma_window: int):
        super().__init__()
        self.__series = series
        self.__short = short_ma_window
        self.__long = long_ma_window
        self._is_valid()

    def generate_signal(self):
        short_ma = MovingAverage(self.__series, self.__short)
        long_ma = MovingAverage(self.__series, self.__long)
        if long_ma.get_moving_average()[-1] > short_ma.get_moving_average()[-1]:
            return 1
        return -1

    def _is_valid(self):
        if len(self.__series) < self.__long:
            raise ValueError("Too long period!")
        if self.__short > self.__long or self.__short < 0:
            raise ValueError("Improper periods lengths!")
        return True
