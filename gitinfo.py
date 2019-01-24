import os
import datetime
import pytz
import re
from email.utils import parsedate_tz
from subprocess import getstatusoutput, run
import subprocess
from pprint import pprint

import csv
import argparse

def grep(needle, haystack):
    assert isinstance(haystack, list)
    return list(filter(lambda k: k.find(needle) >= 0, haystack))

def cmd(s):
    try:
        sts, out = getstatusoutput(s)
    except UnicodeDecodeError:
        # workaround for latin encoded files
        import tempfile
        tmp = tempfile.mktemp()
        cmd("{0} > {1}".format(s, tmp))
        out = open(tmp, encoding="Latin").read()
        os.unlink(tmp)
        sts = 0
    if sts != 0:
        raise Exception("Command error! [{0}] [{1}]", s, out)
    return out

ADDIN = "{+"
ADDOUT = "+}"
SUBIN = "[-"
SUBOUT = "-]"

class Commit:
    def __init__(self, sha1, commiter, date, first=False, merge=False):
        self.sha1 = sha1
        self.commiter = commiter
        try:
            self.date = datetime.datetime(*parsedate_tz(date)[:6], tzinfo=pytz.UTC)
        except:
            self.date = datetime.datetime.now(tz=pytz.UTC)
        self.changes = None
        self.first_commit = first
        self.parse_changes()
        self.merge = merge
        self.blame = {}
        self.dev_porcentage()

    def parse_changes(self):
#        ret = cmd("git log --oneline  --numstat {} -n 1".format(self.sha1))
#        ret = ret.split("\n")[1:]
#        ret = [x.split() for x in ret]
        try:
            ret = cmd("git show {} --word-diff".format(self.sha1)).split("\n")
        except Exception:
            # workaroud for latin encoded files on windows
            import tempfile
            tmp = tempfile.mktemp()
            cmd("git show {0} --word-diff > {1}".format(self.sha1, tmp))
            ret = open(tmp, encoding="Latin").read().split("\n")
            os.unlink(tmp)
        total_add = len(list(filter(lambda k: ADDOUT in k and ADDOUT in k and SUBOUT not in k and SUBOUT not in k, ret)))
        total_sub = len(list(filter(lambda k: ADDOUT not in k and ADDOUT not in k and SUBOUT in k and SUBOUT in k, ret)))
        churn = len(list(filter(lambda k: ADDOUT in k and ADDOUT in k and SUBOUT in k and SUBOUT in k, ret)))


        added_chars = 0
        removed_chars = 0
        churned_chars = 0
        if not self.first_commit:    # TODO ignoring first commit until being able to diff to ... nothing ?
            word_diff = cmd("git diff --word-diff=porcelain {0}~1..{0}".format(self.sha1))
            word_diffs = word_diff.split("~")

            for wd in word_diffs:
                if wd.count("@@") > 2 and wd.count("+++") > 1 and wd.count("---") > 1:
                    continue
                word_list = wd.split("\n")
                try:
                    added = len(list(filter(lambda x: len(x) > 1 and x[0] == "+", word_list))[0].replace(" ", "").replace("\t", ""))
                except Exception:
                    added = 0
                try:
                    removed = len(list(filter(lambda x:len(x) > 1 and x[0] == "-", word_list))[0].replace(" ", "").replace("\t", ""))
                except Exception:
                    removed = 0
                if added > 0 and removed > 0:
                    churned_chars += abs(removed)
                else:
                    added_chars += added
                    removed_chars += removed
        lines_changed = len(cmd("git whatchanged {} -1 --format=oneline".format(self.sha1)).split("\n")[1:])
        self.changes = dict(add=total_add, sub=total_sub, churn=churn,
                            lines=lines_changed,
                            added_chars=added_chars, removed_chars=removed_chars, churned_chars=churned_chars)
        self.dev_porcentage()

    def dev_porcentage(self):
        self.blame = {}
        cmd("git reset --hard")
        cmd("git clean -fdx")
        cmd("git checkout {}".format(self.sha1))
        for file in cmd("git ls-files").split("\n"):
            try:
                blame = cmd("git blame  --line-porcelain {}".format(file)).split("\n")
            except Exception:
                continue# TODO: ignore submodules
            blame = [line[line.rfind("<") + 1:line.rfind(">")] for line in grep('author-mail', blame)]
            for commiter in list(set(blame)):
                if self.blame.get(commiter):
                    self.blame[commiter] += blame.count(commiter)
                else:
                    self.blame[commiter] = blame.count(commiter)


    def __repr__(self):
        return "<Commit {0} {1} {2}>".format(self.sha1, self.commiter, self.date.strftime("%Y-%m-%dT%H:%M:%SZ"))

    def __str__(self):
        return self.__repr__()
    def dict(self):
        d = dict(sha1=self.sha1, commiter=self.commiter,
            date=self.date.strftime("%Y-%m-%dT%H:%M:%SZ"))
        d["changes"] = self.changes
        return d

class Commits(list):
    def load_commits(self, wd=None):
        if wd:
            cwd = os.getcwd()
            os.chdir(wd)
        else:
            cwd = None
        commits = [x.split("|") for x in cmd("git log --pretty=format:\"%h|%ae|%cD\" --since=\"10000 days ago\" ").split("\n")]
        merges = cmd("git log --merges --oneline | cut -d ' ' -f 1").split("\n")
        for commit in commits[:-2]:
            self.append(Commit(*commit, merge=commit[0] in merges))
        self.append(Commit(*commits[-1], first=True))
        if cwd:
            os.chdir(cwd)

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
    def merges(self):
        return len(list(filter(lambda x:x.merge, self)))

    @property
    def accumulated_changes(self):
        d = dict(add=0, sub=0, churn=0, added_chars=0, removed_chars=0, churned_chars=0)
        for commit in self:
            for k in d.keys():
                d[k] += commit.changes[k]
        d["count"] = len(self)
        d["merge"] = self.merges
        return d

    def report(self, date=None):
        if date:
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, "%d/%M/%Y")
            analysis = self.from_date(date)
        else:
            analysis = self
        d = dict()
        for dev in analysis.developers:
            d[dev] = analysis.by_developer(dev).accumulated_changes
        return d

    def report_to_csv(self, filename, date=None):
        report = self.report(date=date)
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["Lines Added", "Lines Removed", "Lines Changed", "Chars added", "Chars removed",
                             "Chars churned", "Total Commits", "Total Merges"])
            for dev in report:
                writer.writerow([dev, report[dev]["add"], report[dev]["sub"], report[dev]["churn"],
                                 report[dev]["added_chars"], report[dev]["removed_chars"], report[dev]["churned_chars"],
                                 report[dev]["count"], report[dev]["merge"]])
        return report

    def report_to_screen(self):
        report = self.report()
        print("|".join(
            ["Developer".rjust(30)] + [x.rjust(15) for x in ["Lines Added", "Lines Removed", "Lines Changed",
                                                             "Chars added", "Chars removed",  "Chars churned",
                                                             "Total Commits", "Total Merges"]]))
        for dev in report:
            print("|".join([dev.rjust(30)] + [str(x).rjust(15) for x in [report[dev]["add"], report[dev]["sub"], report[dev]["churn"],
                                                                         report[dev]["added_chars"],report[dev]["removed_chars"], report[dev]["churned_chars"],
                                                                         report[dev]["count"], report[dev]["merge"]]]))


class Tag:
    def __init__(self, tag, sha1, message, tagger):
        self.tag = tag
        self.sha1 = sha1
        self.tagger = tagger
        self.message = message

class Tags(list):
    def load_tags(self, wd=None):
        if wd:
            cwd = os.getcwd()
            os.chdir(wd)
        else:
            cwd = None
        tags = cmd("git tag").split("\n")
        for tag in tags:
            try:
                taginfo = cmd("git cat-file tag {}".format(tag))
                tagger = re.findall("<([0-9a-zA-Z\._\-]*@[0-9a-zA-Z\._]*)>", taginfo)[0]
                sha1 = re.findall("object *([0-9a-z]*)", taginfo)[0]
                message = taginfo.split("\n")[-1]
                message = message.replace(tag, "").strip()
            except Exception  as e:
                gitlog = cmd("git log -n 1  {}".format(tag))
                sha1 = re.findall("commit *([0-9a-z]*)", gitlog)[0]
                tagger = message = None
            self.append(Tag(tag, sha1, message, tagger))
        if cwd:
            os.chdir(cwd)


if __name__ == "__main__":
    t = Tags()
    t.load_tags("D:\\repo\\roteamento\caronte")
    for x in t:
        assert isinstance(x, Tag)
        print(x.tag, x.sha1, x.tagger, x.message)
    # p = argparse.ArgumentParser("Gitinfo")
    # p.add_argument("--report", help="CSV report file", default=None)
    # p.add_argument("--date", help="Date to start the parse, format : DD/MM/YYYY", default=None)
    # p.add_argument("repos", nargs='+')
    # args = p.parse_args()
    # c = Commits()
    # for repo in args.repos:
    #     c.load_commits(repo)
    # if args.date:
    #     c = c.from_date(date=args.date)
    # c.report_to_screen()
    # if args.report:
    #     c.report_to_csv(args.report)
    #
    #
