import matplotlib.pyplot as plt
import pandas as pd


class AnalyticsBase(object):
    def __init__(self, csv_path: str):
        """
        csv_path is path to database backup in csv
        """
        self._csv_path = csv_path

    def show_plot(self, dataframe: pd.DataFrame):
        """
        allows to show plot of dataframe
        """
        dataframe.plot()
        plt.show()

    def _cleanup_dataframe_from_csv(self):
        df = pd.read_csv(self._csv_path, dtype=object, delimiter='|', index_col='id')
        for index, row in df.iterrows():
            row['user_stocks'] = str(row['user_stocks']).split(',')
            row['user_cryptos'] = str(row['user_cryptos']).split(',')
            row['user_currencies'] = str(row['user_currencies']).split(',')
            row['user_resources'] = str(row['user_resources']).split(',')
        return df
