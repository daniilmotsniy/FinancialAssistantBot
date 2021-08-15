import json

import matplotlib.pyplot as plt
import pandas as pd


def assets_total_count(file_path: str) -> dict:
    raw_data = pd.read_csv(file_path)
    raw_assets = raw_data['user_assets']
    frames = []

    for ass in raw_assets:
        frames.append(pd.DataFrame.from_dict(json.loads(ass), orient='index').transpose())

    result = pd.concat(frames)

    total = dict(result.count())

    # this plot shows count of assets by each type from all users
    # total.plot()
    # plt.show()

    return total
