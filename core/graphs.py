from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

from graphos.renderers import yui



def get_graph(repository, days, type="log", draw="pie"):
    from .datasource import CommitsByDeveloperLog, CommitsByDeveloper
    from .models import Commit

    periodo_start = datetime.today() - timedelta(days=int(days))
    queryset = Commit.objects.filter(repository=repository, date__gte=periodo_start)
    type_function = {
        "log":CommitsByDeveloperLog,
        "normal":CommitsByDeveloper
    }
    datasource = type_function[type](queryset=queryset, fields=['commiter', 'add', 'sub', 'churn'])
    draw_function = {
        "bar": yui.BarChart,
        "pie": yui.PieChart
    }
    return draw_function[draw](datasource)


# Libraries
def radar_plot(filename, data):
    pass
    # Set data
    for k in data:
        if not isinstance(data[k], list):
            data[k] = [data[k]]
    df = pd.DataFrame.from_dict(data)
    # number of variable
    categories = list(df)
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = df.loc[0].values.flatten().tolist()
    values += values[:1]

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

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.savefig(filename)

if __name__ == '__main__':
    data = {'merges': 4, 'char_sub': 863, 'sub': 863, 'sum': 33431, 'char_churn': 519, 'churn': 519, 'char_sum': 33431}
    radar_plot("/tmp/radar.png", data)