import logging

import requests
from prettytable import PrettyTable

from telegram_bot.config import FINFUB_TOKEN
from telegram_bot.public_api.base import BaseTelegram


class StocksApi(BaseTelegram):
    def get_table(self, tickers):
        """
        :param tickers: list of companies will be shown ['AAPL', 'BA']
        :return: PrettyTable class
        """
        table = PrettyTable()
        table.field_names = ["Name", "Price $"]

        for ticker in tickers:
            # TODO refactor try except
            try:
                price = requests.get('https://finnhub.io/api/v1/quote?symbol='
                                     + ticker + '&token=' + FINFUB_TOKEN).json()['c']
                table.add_row([ticker, price])
            except Exception as e:
                logging.error(e)
        return table
