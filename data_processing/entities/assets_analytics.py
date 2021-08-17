import json

import pandas as pd

from .analytics_base import AnalyticsBase


class AssetsAnalytics(AnalyticsBase):
    def __init__(self, csv_path: str):
        """
        csv_path is path to database backup in csv
        """
        self._csv_path = csv_path

    def assets_total_count(self) -> dict:
        """
        allows to get count of total assets in users
        """
        raw_data = pd.read_csv(self._csv_path)
        raw_assets = raw_data['user_assets']
        frames = []

        for asset in raw_assets:
            frames.append(pd.DataFrame.from_dict(json.loads(asset), orient='index').transpose())

        result = pd.concat(frames)

        return dict(result.count())

    def stocks_total_count(self) -> dict:
        """
        allows to get count per different stocks from users
        """
        raw_data = pd.read_csv(self._csv_path)
        raw_assets = raw_data['user_assets']
        frames = []

        for asset in raw_assets:
            frames.append(pd.DataFrame.from_dict(json.loads(asset), orient='index').transpose())

        result = pd.concat(frames)

        return dict(result.count())
