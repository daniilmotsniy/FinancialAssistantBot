# COPY users TO 'C:\Files\test_users.csv' DELIMITER ',' CSV HEADER;
import json

import matplotlib.pyplot as plt
import pandas as pd

raw_data = pd.read_csv('test_users.csv')
raw_assets = raw_data['user_assets']

frames = []

for ass in raw_assets:
    frames.append(pd.DataFrame.from_dict(json.loads(ass), orient='index').transpose())

result = pd.concat(frames)

# this plot shows count of assets by each type from all users
result.count().plot()

plt.show()