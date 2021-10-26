import pandas as pd

from collections import defaultdict
from typing import Dict, List, Any

from . import AnalyticsBase


class AssetsAnalytics(AnalyticsBase):
    def __init__(self, csv_path: str):
        """
        csv_path is path to database backup in csv
        """
        self.df = self._cleanup_dataframe_from_csv(csv_path)

    def _cleanup_dataframe_from_csv(self, csv_path: str):
        df = pd.read_csv(csv_path, dtype=object, delimiter='|', index_col='id')
        for index, row in df.iterrows():
            row['user_stocks'] = str(row['user_stocks']).split(',')
            row['user_cryptos'] = str(row['user_cryptos']).split(',')
            row['user_currencies'] = str(row['user_currencies']).split(',')
            row['user_resources'] = str(row['user_resources']).split(',')
        return df

    def assets_total_count(self) -> dict:
        """
        allows to get count of total assets in users
        """
        result = defaultdict(lambda: 0)
        for index, row in self.df.iterrows():
            result['user_stocks'] += len(row['user_stocks'])
            result['user_cryptos'] += len(row['user_cryptos'])
            result['user_currencies'] += len(row['user_currencies'])
            result['user_resources'] += len(row['user_resources'])

        return result

    def asset_total_count(self, asset: str) -> List[Dict[str, Any]]:
        """
        asset [str]: it could be 'user_stocks'
        allows to get count per different asset from users
        """
        total = self.df[asset].explode().value_counts().rename_axis('label').reset_index(name='count')
        return [{'label': v['label'], 'count': v['count']}
                for k, v in total.iterrows()]
