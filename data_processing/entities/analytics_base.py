import matplotlib.pyplot as plt
import pandas as pd


class AnalyticsBase(object):
    def show_plot(self, dataframe: pd.DataFrame):
        """
        allows to show plot of dataframe
        """
        dataframe.plot()
        plt.show()
