import datetime
import calendar

from itertools import zip_longest

class ChartData:
    """
        Stores an item to be stored in a chart's dataset.
    """

    def __init__(self, label="", data=[]):
        self.label = label
        self.data = data 

    def toJson(self):
        """
            Returns the Json format so that the chart class can
            use it in it's own toJson method.
        """
        return {
            "label": self.label,
            "data": self.data,
            "lineTension": 0
        }


class Chart:
    """
        A simple chart class that has some useful methods.
    """

    def __init__(self, chart_type="line", labels=[], datasets=[]):
        self.chart_type = chart_type
        self.labels = labels
        self.datasets = datasets

    def add_data(self, chart_data):
        """
            Simply adds the chart_data object to the datasets list
        """
        self.datasets.append(chart_data)

    def alter_from_df(self, df, rule=lambda x, y: x):
        """
            Gets the data from the given data frame and 
            alters the first ChartData object in the datasets list.
            It uses the lambda argument 'rule' to decide what to do
            with the old and new values
        """
        rows = [df.iloc[i] for i in range(len(df))]
        # for each row in the data frame, get the date then
        # convert it to a weekday name and get the first three letters
        dates = [r.name for r in rows]
        self.labels = [calendar.day_name[x.weekday()][:3] for x in dates],
        # get the closing prices for each row
        new_values = [r.Close for r in rows]
        # make sure there's a chart data object in the datasets
        if len(self.datasets) == 0:
            self.datasets.append(ChartData())
        zipped = list(zip_longest(new_values, self.datasets[0].data))
        # write the new values to the chart data in datasets[0] using
        # the rule lambda to decide what to do with the new and old values
        self.datasets[0].data = [rule(t[0], t[1]) for t in zipped]

    def getJson(self):
        """
            Returns this chart's valid json format so that
            javascript can interpret it.
        """
        return {
            "type": self.chart_type,
            "data": {
                "labels": self.labels,
                "datasets": [d.toJson() for d in self.datasets]
            }
        }