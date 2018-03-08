import datetime
import calendar

from itertools import zip_longest

class ChartData:
    """
        Stores an item to be stored in a chart's dataset.
    """

    def __init__(self, label="", data=None):
        self.label = label
        if data:
            self.data = data 
        else:
            self.data = []

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

    def __init__(self, chart_type="line", labels=None, datasets=None):
        self.chart_type = chart_type
        if labels:
            self.labels = labels
        else: 
            self.labels = []
        if datasets:
            self.datasets = datasets
        else: 
            self.datasets = []

    def add_data(self, chart_data):
        """
            Simply adds the chart_data object to the datasets list
        """
        self.datasets.append(chart_data)

    def add_from_sh(self, label, hists):
        """
            Adds a new ChartData object to the list of datasets
            from the stock history list
        """
        dates = [h.date for h in hists]
        if len(dates) <= 6:
            self.labels = [calendar.day_name[x.weekday()][:3] for x in dates]
        else:
            self.labels = [x.day for x in dates]
        new_values = [h.close_price for h in hists]
        chart_data= ChartData(label=label, data=new_values)
        self.datasets.append(chart_data)


    def alter_from_sh(self, hists, set_loc=0, rule=lambda x, y: x):
        """
            Gets the data from the given DataFrame and 
            alters the ChartData object at index 'set_loc' in the datasets list.
            It uses the lambda argument 'rule' to decide what to do
            with the old and new values.
            This does not alter the labels of the chart, as it assumes the dates in
            the dataframe are consistent with the current labels.
        """
        # get the closing prices for each day
        new_values = [h.close_price for h in hists]
        # make sure there's a chart data object in the datasets
        zipped = list(zip_longest(new_values, self.datasets[set_loc].data, fillvalue=0))
        # write the new values to the chart data in datasets[0] using
        # the rule lambda to decide what to do with the new and old values
        self.datasets[set_loc].data = [rule(t[0], t[1]) for t in zipped]


    def toJson(self):
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