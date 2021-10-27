from abc import ABCMeta

from prettytable import PrettyTable


class BaseTelegram(metaclass=ABCMeta):
    def get_table(self, tickers: list) -> PrettyTable:
        pass
