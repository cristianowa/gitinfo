from graphos.sources.model import ModelDataSource


class CommitsByDeveloper(ModelDataSource):
    def get_data(self):
        data = super(CommitsByDeveloper, self).get_data()
        header = data[0]
        data_without_header = data[1:]
        d = {}
        for row in data_without_header:
            commiter = str(row[0].email)
            add = row[1]
            sub = row[2]
            churn = row[3]
            if commiter not in d.keys():
                d[commiter] = [commiter, add, sub, churn]
            else:
                d[commiter][1] += add
                d[commiter][2] += sub
                d[commiter][3] += churn
        data_without_header = list(d.values())
        data_without_header = [(x[0], x[1], x[2], x[3]) for x in data_without_header]
        data_without_header.insert(0, header)
        return data_without_header


class CommitsByDeveloperLog(ModelDataSource):
    def get_data(self):
        data = super(CommitsByDeveloperLog, self).get_data()
        header = data[0]
        data_without_header = data[1:]
        d = {}
        for row in data_without_header:
            commiter = str(row[0].email)
            add = row[1]
            sub = row[2]
            churn = row[3]
            if commiter not in d.keys():
                d[commiter] = [commiter, add, sub, churn]
            else:
                d[commiter][1] += add
                d[commiter][2] += sub
                d[commiter][3] += churn
        def log(k):
            from math import log as log_
            try:
                return log_(float(k))
            except Exception:
                return 0
        data_without_header = list(d.values())
        data_without_header = [(x[0], log(x[1]), log(x[2]), log(x[3])) for x in data_without_header]
        data_without_header.insert(0, header)
        return data_without_header