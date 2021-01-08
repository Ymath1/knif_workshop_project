from itertools import product
from knif_workshop_project.modules.strategies import Strategy
from knif_workshop_project.modules.back_test import MultipleBackTest
from knif_workshop_project.modules.performance_statistics import PerformanceStatistics


class BackTestController:

    def __init__(self):
        pass

    def run(self, strategy: Strategy, data, n, returns, **kwargs):
        list_of_strategies = []
        options = self.__create_all_options(kwargs)
        for option in options:
            list_of_strategies.append(strategy(**option))
        results = MultipleBackTest(list_of_strategies, data, n).back_test()
        return self.__get_multiple_statistics(returns, results)

    @staticmethod
    def __create_all_options(option_dict):
        return list(dict(zip(option_dict.keys(), values)) for values in product(*option_dict.values()))

    def __get_multiple_statistics(self, returns, results):
        statistics = {}
        for k, v in results.items():
            statistics[k] = self.__get_statistics(returns, v)
        return statistics

    @staticmethod
    def __get_statistics(returns, strategy_signals):
        strategy_returns = returns.signals_to_returns(strategy_signals)
        statistics = PerformanceStatistics(strategy_returns).get_full_statistics()
        return statistics

