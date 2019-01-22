from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import mpld3

from graphos.renderers import yui


def get_graph(repository, days, type="log", draw="pie"):
    from .datasource import CommitsByDeveloperLog, CommitsByDeveloper
    from .models import Commit

    periodo_start = datetime.today() - timedelta(days=int(days))
    queryset = Commit.objects.filter(repository=repository, date__gte=periodo_start)
    type_function = {
        "log": CommitsByDeveloperLog,
        "normal": CommitsByDeveloper
    }
    datasource = type_function[type](queryset=queryset, fields=['commiter', 'add', 'sub', 'churn'])
    draw_function = {
        "bar": yui.BarChart,
        "pie": yui.PieChart
    }
    return draw_function[draw](datasource)


# Libraries
def radar_plot(filename, data, labels=None):
    plt.rcParams["figure.figsize"] = 10, 6
    # Set data
    if isinstance(data, list):
        full_data = data
    else:
        full_data = [data]
    for data in full_data:
        for k in data:
            if not isinstance(data[k], list):
                data[k] = [data[k]]
    df = pd.DataFrame.from_dict(full_data[0])
    # number of variable
    categories = list(df)
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.clf()
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1, 2.5, 5], ["10%", "50%", "100%"], color="grey", size=7)
    plt.ylim(0, 5)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    for i, data in zip(range(len(full_data)), full_data):
        df = pd.DataFrame.from_dict(data)
        values = df.loc[0].values.flatten().tolist()
        values += values[:1]

        if labels:
            label = labels[i]
        else:
            label = None
        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=label)

        # Fill area
        ax.fill(angles, values, alpha=0.1)
    # Add legend
    # plt.legend(loc='upper right', bbox_to_anchor=(0.3, 0.1))
    plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    plt.savefig(filename)


def test_radar():
    data1 = {'merges': 1, 'char_sub': 1, 'sub': 2, 'sum': 4, 'char_churn': 1, 'churn': 2, 'char_sum': 5}
    data2 = {'merges': 2, 'char_sub': 3, 'sub': 1, 'sum': 5, 'char_churn': 4, 'churn': 3, 'char_sum': 2}
    radar_plot("/tmp/radar.png", [data1, data2], labels=["um", "dois"])


def time_series(filename, data):
    import collections
    import numpy as np
    import matplotlib.pyplot as plt
    # plt.rcParams["figure.figsize"] = 15, 6
    df = pd.DataFrame.from_dict(data)
    print(df.to_csv())
    df = df.transpose()
    print(df.to_csv())
    df.plot()
    plt.savefig(filename)


def test_timeseries():
    d = {datetime(2018, 12, 27,  6, 59): {'add': 1, 'char_add': 10, 'char_churn':  4, 'sub': 0, 'churn': 2, 'char_sub': 10},
         datetime(2018, 12, 28, 16, 59): {'add': 2, 'char_add': 30, 'char_churn': 70, 'sub': 1, 'churn': 1, 'char_sub': 30},
         datetime(2018, 12, 29,  3, 59): {'add': 5, 'char_add': 40, 'char_churn': 30, 'sub': 0, 'churn': 2, 'char_sub': 20},
         datetime(2018, 12, 30, 16, 00): {'add': 7, 'char_add': 35, 'char_churn': 50, 'sub': 9, 'churn': 3, 'char_sub': 40},
         datetime(2019,  1,  1, 16, 15): {'add': 9, 'char_add': 15, 'char_churn': 70, 'sub': 0, 'churn': 2, 'char_sub': 10},
         datetime(2019,  1,  4, 16, 59): {'add': 8, 'char_add': 75, 'char_churn': 90, 'sub': 8, 'churn': 3, 'char_sub': 20},
         datetime(2019,  1,  6, 16, 27): {'add': 4, 'char_add': 10, 'char_churn': 70, 'sub': 0, 'churn': 2, 'char_sub': 30}
        }
    time_series("", d)

if __name__ == '__main__':
    # test_radar()
    test_timeseries()
    pass

