import csv
import json

import pandas as pd

raw_data = pd.read_csv('../test_data/test_users.csv')
raw_assets = raw_data['user_assets']

with open('../test_data/test_data.csv', 'w') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerow(['id', 'user_stocks', 'user_cryptos', 'user_currencies', 'user_resources'])
    id = 0
    for asset in raw_assets:
        stocks = ",".join(json.loads(asset)['user_stocks'])
        cryptos = ",".join(json.loads(asset)['user_cryptos'])
        currencies = ",".join(json.loads(asset)['user_currencies'])
        resources = ",".join(json.loads(asset)['user_resources'])
        writer.writerow([id, stocks, cryptos, currencies, resources])
        id += 1

