import datetime
from email.utils import parsedate_tz
from subprocess import getstatusoutput
from pprint import pprint
import csv

import path
from exdict import Exdict

def cmd(s):
    sts, out = getstatusoutput(s)
    if sts != 0:
        raise Exception("Command error! [{0}] [{1}]", s, out)
    return out

ADDIN = "{+"
ADDOUT = "+}"
SUBIN = "[-"
SUBOUT = "-]"

class Commit:
    def __init__(self, sha1, commiter, date):
        self.sha1 = sha1
        self.commiter = commiter
        try:
            self.date = datetime.datetime(*parsedate_tz(date)[:6])
        except:
            self.date = datetime.datetime.now()
        self.changes = None
        self.parse_changes()

    def parse_changes(self):
#        ret = cmd("git log --oneline  --numstat {} -n 1".format(self.sha1))
#        ret = ret.split("\n")[1:]
#        ret = [x.split() for x in ret]
        ret = cmd("git show {} --word-diff".format(self.sha1)).split("\n")
        total_add = len(list(filter(lambda k: ADDOUT in k and ADDOUT in k and SUBOUT not in k and SUBOUT not in k, ret)))
        total_sub = len(list(filter(lambda k: ADDOUT not in k and ADDOUT not in k and SUBOUT in k and SUBOUT in k, ret)))
        churn = len(list(filter(lambda k: ADDOUT in k and ADDOUT in k and SUBOUT in k and SUBOUT in k, ret)))
        self.changes = Exdict(add=total_add, sub=total_sub, churn=churn)


    def __repr__(self):
        return "<Commit {0} {1} {2}>".format(self.sha1, self.commiter, self.date.strftime("%Y-%m-%dT%H:%M:%SZ"))

    def __str__(self):
        return self.__repr__()
    def dict(self):
        d = dict(sha1=self.sha1, commit=self.commiter, 
            date=self.date.strftime("%Y-%m-%dT%H:%M:%SZ"))
        d["changes"] = self.changes
        return d

class Commits(list):
    def load_commits(self, wd=None):
        wd = wd or path.getcwdu()
        with path.Path(wd):
            commits = [x.split("|") for x in cmd("git log --pretty=format:\"%h|%ae|%cD\" --since=\"300 days ago\" ").split("\n")]
            for commit in commits:
                self.append(Commit(*commit))

    def dict(self):
        return [x.dict() for x in self]

    def from_date(self, date):
        return Commits(filter(lambda k: k.date > date, self))

    def by_developer(self, commiter):
        return Commits(filter(lambda k: k.commiter == commiter, self))

    @property
    def developers(self):
        return list(set([x.commiter for x in self]))

    @property
    def accumulated_changes(self):
        d = Exdict(add=0, sub=0, churn=0)
        for commit in self:
            d.add += commit.changes.add
            d.sub += commit.changes.sub
            d.churn += commit.changes.churn
        d.count = len(self)
        return d

    def report(self, date=None):
        if date:
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, "%d/%M/%Y")
            analysis = self.from_date(date)
        else:
            analysis = self
        d = Exdict()
        for dev in analysis.developers:
            d[dev] = analysis.by_developer(dev).accumulated_changes
        return d

    def report_to_csv(self, filename, date=None):
        report = self.report(date=date)
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["Developer", "Lines Added", "Lines Removed", "Lines Changed", "Total Commits"])
            for dev in report:
                writer.writerow([dev, report[dev].add, report[dev].sub, report[dev].churn, report[dev].count])
        return report


if __name__ == "__main__":
    c = Commits()
    c.load_commits("/home/cristiano/repo/gitinfo/")
    # pprint(c.from_date(datetime.datetime(2018,11,1)).dict())
    # print(c.developers)
    # pprint(c.by_developer(c.developers[0]).dict())
    # pprint(c.by_developer(c.developers[0]).accumulated_changes)
    pprint(c.report(date="01/10/2018"))
    c.report_to_csv('/tmp/teste.csv', date="01/10/2018")

