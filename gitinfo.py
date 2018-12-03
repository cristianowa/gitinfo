import datetime
from email.utils import parsedate_tz
from subprocess import getstatusoutput
from pprint import pprint

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
    def accumalated_changes(self):
        d = Exdict(add=0, sub=0, churn=0)
        for commit in self:
            d.add += commit.add
            d.sub += commit.sub
            d.churn += d.churn
        return d

if __name__ == "__main__":
    c = Commits()
    c.load_commits("/home/cristiano/repo/gitinfo/")
    pprint(c.dict())
    pprint(c.from_date(datetime.datetime(2018,11,1)).dict())
    print(c.developers)
    pprint(c.by_developer(c.developers[0]).dict())
