from beartype import beartype
from knif_workshop_project.modules.data_handling import MovingAverage


class Strategy:

    def __init__(self):
        pass

    def generate_signal(self, data):
        raise NotImplementedError("Method must be overridden in the derived class!")

    def slice_data(self, data, start, end):
        raise NotImplementedError("Method must be overridden in the derived class!")

    def representation(self):
        raise NotImplementedError("Method must be overridden in the derived class!")

    def _is_valid(self, data):
        raise NotImplementedError("Method must be overridden in the derived class!")


class BuyHoldStrategy(Strategy):

    @beartype
    def __init__(self):
        super().__init__()

    def generate_signal(self, data):
        self._is_valid(data)
        return 1

    def slice_data(self, data, start, end):
        return data

    def representation(self):
        return "BuyHold Strategy"

    def _is_valid(self, data):
        if len(data) > 0:
            return True
        raise ValueError("Series has to contain any observation!")


class ReversalStrategy(Strategy):

    @beartype
    def __init__(self):
        super().__init__()

    def generate_signal(self, data):
        self._is_valid(data)
        return -1 if data.calculate_returns()[-1] > 0 else 1

    def slice_data(self, data, start, end):
        return data.slice_data(start, end)

    def representation(self):
        return "Reversal Strategy"

    def _is_valid(self, data):
        if len(data) > 0:
            return True
        raise ValueError("Series has to contain any observation!")


class MovingAverageCrossoverStrategy(Strategy):

    @beartype
    def __init__(self, short_ma_window: int, long_ma_window: int):
        super().__init__()
        self.__short = short_ma_window
        self.__long = long_ma_window

    def generate_signal(self, data):
        self._is_valid(data)
        short_ma = MovingAverage(data, self.__short)
        long_ma = MovingAverage(data, self.__long)
        if long_ma.get_moving_average()[-1] > short_ma.get_moving_average()[-1]:
            return 1
        return -1

    def slice_data(self, data, start, end):
        return data.slice_data(start, end)

    def representation(self):
        return f"MA Crossover Long: {self.__long} Short: {self.__short}"

    def _is_valid(self, data):
        if len(data) < self.__long:
            raise ValueError("Too short period!")
        if self.__short > self.__long or self.__short < 0:
            raise ValueError("Improper periods lengths!")
        return True