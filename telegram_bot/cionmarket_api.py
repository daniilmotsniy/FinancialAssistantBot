from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from prettytable import PrettyTable
from config import COIN_MARKET_TOKEN

crypto_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

crypto_parameters = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COIN_MARKET_TOKEN,
}

session = Session()
session.headers.update(headers)


def get_crypto_data(symbol_: list):
    """
    :param symbol_: list that contains only needed cryptos ['BTC', ...]
    :return: PrettyTable class
    """
    try:
        response = session.get(crypto_url, params=crypto_parameters)
        data = json.loads(response.text)
        table = PrettyTable()
        table.field_names = ["Name", "Price $", "Change %"]

        for d in data['data']:
            if d['symbol'] in symbol_:
                percent_change_24h = str(round(d['quote']['USD']['percent_change_24h'], 2))
                if percent_change_24h.startswith('-'):
                    icon = ' \U0001F534'
                else:
                    icon = ' \U0001F7E2'
                table.add_row([d['symbol'], round(d['quote']['USD']['price'], 2),
                               percent_change_24h + icon])
        return table

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

