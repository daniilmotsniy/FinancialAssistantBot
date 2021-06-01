import json

import requests
from prettytable import PrettyTable


def get_fiat_data(cc_: list):
    """
    :param cc_: list that contains only needed cc ['USD', ...]
    :return: PrettyTable class
    """
    try:
        data = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()

        table = PrettyTable()

        table.field_names = ["Fiat", "Price"]

        for d in data:
            if d['cc'] in cc_:
                table.add_row([d['txt'], round(d['rate'], 2)])
        # print(table)
        return table

    except Exception as e:
        print(e)