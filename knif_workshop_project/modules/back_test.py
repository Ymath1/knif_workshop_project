from beartype import beartype

from knif_workshop_project.modules.strategies import Strategy


class BackTest:

    @beartype
    def __init__(self, strategy: Strategy, data, n=250):
        self.__strategy = strategy
        self.__data = data
        self.__n = n

    def back_test(self):
        length = len(self.__data)
        signals = [0] * self.__n
        for i in range(self.__n, length):
            sliced = self.__strategy.slice_data(self.__data, i-self.__n, i+1)
            signal = self.__strategy.generate_signal(sliced)
            signals.append(signal)
        return signals


class MultipleBackTest:

    @beartype
    def __init__(self, list_of_strategies, data, n=250):
        self.__list_of_strategies = list_of_strategies
        self.__data = data
        self.__n = n

    def back_test(self):
        signals = {}
        for strategy in self.__list_of_strategies:
            signals[strategy.representation()] = BackTest(strategy, self.__data, self.__n).back_test()
        return signals




