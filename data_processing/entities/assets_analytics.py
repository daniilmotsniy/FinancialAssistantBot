from collections import defaultdict
from typing import Dict, List, Any

from . import AnalyticsBase


class AssetsAnalytics(AnalyticsBase):
    def __init__(self, csv_path: str):
        super().__init__(csv_path)
        # main dataframe from csv
        self.df = self._cleanup_dataframe()

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
