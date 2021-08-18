from collections import defaultdict

from . import AnalyticsBase


class AssetsAnalytics(AnalyticsBase):
    def assets_total_count(self) -> dict:
        """
        allows to get count of total assets in users
        """
        df = self._cleanup_dataframe()
        result = defaultdict(lambda: 0)

        for index, row in df.iterrows():
            result['user_stocks'] += len(row['user_stocks'])
            result['user_cryptos'] += len(row['user_cryptos'])
            result['user_currencies'] += len(row['user_currencies'])
            result['user_resources'] += len(row['user_resources'])

        return result

    def stocks_total_count(self) -> dict:
        """
        allows to get count per different stocks from users
        """
        df = self._cleanup_dataframe()
        result = {}
        for index, row in df.iterrows():
            result['label'] = 'test'
            result['value'] = 1
            # print(row['user_stocks'].count())
        return {'item': result}
