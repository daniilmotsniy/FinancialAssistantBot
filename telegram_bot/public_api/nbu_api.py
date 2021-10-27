import logging

import requests
from prettytable import PrettyTable

from telegram_bot.public_api.base import BaseTelegram


class CurrenciesApi(BaseTelegram):
    def get_table(self, tickers):
        try:
            response = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/'
                                    'exchange?json').json()
            table = PrettyTable()
            table.field_names = ["Fiat", "Price"]

            for currency in response:
                if currency['cc'] in tickers:
                    table.add_row([currency['txt'], round(currency['rate'], 2)])
            return table

        except Exception as e:
            logging.error(e)