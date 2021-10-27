import logging

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from prettytable import PrettyTable

from telegram_bot.config import COIN_MARKET_TOKEN
from telegram_bot.public_api.base import BaseTelegram

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

PARAMS = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COIN_MARKET_TOKEN,
}

session = Session()
session.headers.update(HEADERS)


class CryptoApi(BaseTelegram):
    def get_table(self, tickers):
        """
        :param tickers: list that contains only needed cryptos ['BTC', ...]
        :return: PrettyTable class
        """
        table = PrettyTable()
        try:
            response = session.get(API_URL, params=PARAMS)
            response = json.loads(response.text)
            table.field_names = ["Name", "Price $", "Change %"]

            for ticker in response['data']:
                if ticker['symbol'] in tickers:
                    percent_change_24h = str(round(ticker['quote']['USD']['percent_change_24h'], 2))
                    if percent_change_24h.startswith('-'):
                        icon = ' \U0001F534'
                    else:
                        icon = ' \U0001F7E2'
                    table.add_row([ticker['symbol'], round(ticker['quote']['USD']['price'], 2),
                                   percent_change_24h + icon])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logging.error(e)
        return table

