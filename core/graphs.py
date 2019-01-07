from datetime import datetime, timedelta

from graphos.renderers import yui

from core.datasource import CommitsByDeveloperLog, CommitsByDeveloper
from core.models import Commit


def get_graph(repository, days, type="log", draw="pie"):
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