from os import environ as env
import requests
from prettytable import PrettyTable

from config import FINFUB_TOKEN

TOKEN = FINFUB_TOKEN


def get_stock_data(ticker_):
    """
    :param ticker_: list of companies will be shown
    :return: PrettyTable class
    """
    table = PrettyTable()
    table.field_names = ["Name", "Price $"]

    for c in ticker_:
        try:
            r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + c + '&token=' + TOKEN)
            table.add_row([c, r.json()['c']])
        except Exception as e:
            print(e)
    return table
