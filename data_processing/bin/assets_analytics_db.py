import logging
from collections import defaultdict
from typing import Dict, List, Any

from . import AnalyticsBase
from data_processing.gateways import postgres
from data_processing.entity import asset


class AssetsAnalytics(AnalyticsBase):
    def __init__(self):
        super().__init__()
        self.assets_obj = self._read_from_db()

    def assets_total_count(self) -> dict:
        """
        allows to get count of total assets in users
        """
        result = defaultdict(lambda: 0)
        for asset in self.assets_obj:
            logging.warning(asset.user_stocks)
            result['user_stocks'] += len(asset.user_stocks)
            result['user_cryptos'] += len(asset.user_cryptos)
            result['user_currencies'] += len(asset.user_currencies)
            result['user_resources'] += len(asset.user_resources)

        return result

    # def asset_total_count(self, asset: str) -> List[Dict[str, Any]]:
    #     """
    #     asset [str]: it could be 'user_stocks'
    #     allows to get count per different asset from users
    #     """
    #     total = self.df[asset].explode().value_counts().rename_axis('label').reset_index(name='count')
    #     return [{'label': v['label'], 'count': v['count']}
    #             for k, v in total.iterrows()]

    def _read_from_db(self):
        return postgres.Postgres().session().query(asset.Asset).all()
