import re
import os
from enum import Enum
from datetime import datetime, timedelta

from django.db import models

# Create your models here.


class Commiter(models.Model):
    email = models.CharField(max_length=100, unique=True)
    def __repr__(self):
        return "< {email} >".format(email=self.email)

    def __str__(self):
        return self.__repr__()

    @property
    def commits(self):
        return CommitList(Commit.objects.filter(commiter=self))

    def filter_commits(self, **kwargs):
        return CommitList(Commit.objects.filter(commiter=self, **kwargs))

    def update(self):
       CommitsMetrics.objects.filter(commiter=self).delete()
       for period in PeriodChoice:
            days = re.findall("[0-9]+", period.name)[0]
            period_start = datetime.today() - timedelta(days=int(days))
            commit_list = CommitList(Commit.objects.filter(commiter=self, date__gte=period_start))
            repos = list(set([c.repository.url for c in commit_list]))
            commit_metrics = CommitsMetrics(add=commit_list.add,
                                            sub=commit_list.sub,
                                            churn=commit_list.churn,
                                            char_add=commit_list.char_add,
                                            char_sub=commit_list.char_sub,
                                            char_churn=commit_list.char_churn,
                                            merges=commit_list.merges,
                                            commiter=self,
                                            repositories=len(repos),
                                            period=period
                                            )
            commit_metrics.save()

    @property
    def repositories(self):
        commits = Commit.objects.filter(commiter=self)
        return list(set([c.repository for c in commits]))

    @property
    def metrics(self):
        return CommitsMetrics.metrics_developer(self)

    @property
    def metrics_normalized(self):
        return CommitsMetrics.metrics_norm_developer(self)


    @property
    def report(self):
        d = dict()
        d["metrics"] = self.metrics
        d["metrics_normalized"] = self.metrics_normalized
        d["repositories"] = [r.dict() for r in self.repositories]
        return d

class CommitList(list):
    @property
    def add(self):
        return sum([commit.add for commit in self])

    @property
    def sub(self):
        return sum([commit.sub for commit in self])

    @property
    def churn(self):
        return sum([commit.churn for commit in self])

    @property
    def char_add(self):
        return sum([commit.char_add for commit in self])

    @property
    def char_sub(self):
        return sum([commit.char_sub for commit in self])

    @property
    def char_churn(self):
        return sum([commit.char_churn for commit in self])

    @property
    def merges(self):
        return len(list(filter(lambda commit:commit.merge, self)))

    @property
    def metrics(self):
        return dict(add=self.add, sub=self.sub, churn=self.churn, merges=self.merges,
                    char_sadd=self.char_add, char_sub=self.char_sub, char_churn=self.char_churn)

class Repository(models.Model):
    url = models.CharField(max_length=256, unique=True)
    branch = models.CharField(max_length=256, default="master")
    def update(self):
        from gitinfo import cmd
        import shutil
        import gitinfo
        import tempfile
        tmp = tempfile.mkdtemp()
        cmd("git clone {0} {1}".format(self.url, tmp))
        oldwd = os.getcwd()
        os.chdir(tmp)
        cmd("git checkout origin/{}".format(self.branch))
        cmd("git checkout -B {}".format(self.branch))
        commits = gitinfo.Commits()
        commits.load_commits(tmp)
        for commit in commits:
            try:
                dbcommit = Commit.objects.get(sha1=commit.sha1)
            except Commit.DoesNotExist:
                # now we create it
                try:
                    commiter = Commiter.objects.get(email=commit.commiter)
                except Commiter.DoesNotExist:
                    commiter = Commiter(email=commit.commiter)
                    commiter.save()
                commit.parse_changes()
                dbcommit = Commit(sha1=commit.sha1,
                                  repository=self,
                                  commiter=commiter,
                                  date=commit.date.strftime("%Y-%m-%d %H:%M"),
                                  add=commit.changes["add"],
                                  sub=commit.changes["sub"],
                                  churn=commit.changes["churn"],
                                  char_add=commit.changes["added_chars"],
                                  char_sub=commit.changes["removed_chars"],
                                  char_churn=commit.changes["churned_chars"],
                                  merge=commit.merge)
                dbcommit.save()

        cmd("git submodule init")
        cmd("git submodule update")
        modules_urls = cmd("git submodule foreach \"git ls-remote --get-url\"").split("\n")
        modules = list(filter(lambda k: "Entering '" not in k, modules_urls))
        for mod in modules:
            if len(Submodule.objects.filter(holder=self, url=mod)) == 0 and mod != '':
                candidate = Repository.objects.filter(url=mod)
                if len(candidate) == 1:
                    submodule_repo = candidate[0]
                else:
                    submodule_repo = None
                try:
                    submodule = Submodule.objects.get(holder=self, url=mod)
                except Submodule.DoesNotExist:
                    submodule = Submodule(holder=self, url=mod)
                if submodule_repo:
                    submodule.dependency = submodule_repo
                submodule.save()

            # TODO: remove removed submddules

        tags = gitinfo.Tags()
        tags.load_tags(tmp)
        for tag in tags:
            if tag.tagger:
                commiter = Commiter.objects.get(email=tag.tagger)
            else:
                commiter = None
            try:
                commit = Commit.objects.get(sha1=tag.sha1[:7])
            except Commit.DoesNotExist:
                print("Error : {}".format(tag.sha1[:7]))
                continue # tags without commit are out of main branch and are not computed
            t = Tag(commiter=commiter,
                    commit=commit,
                    name=tag.tag, message=tag.message)
            t.save()
        os.chdir(oldwd)
        shutil.rmtree(tmp, ignore_errors=True)

    def __repr__(self):
        return "< {url} >".format(url=self.url)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return dict(url=self.url)

    @property
    def commits(self):
        return CommitList(Commit.objects.filter(repository=self))

    def filter_commits(self, **kwargs):
        return CommitList(Commit.objects.filter(repository=self, **kwargs))

    @property
    def depended_by(self):
        return [x.holder for x in Submodule.objects.filter(dependency=self)]

    @property
    def depends_of(self):
        return [x.dependency for x in Submodule.objects.filter(holder=self)]


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    date = models.DateTimeField(default="1990-01-01 09:30")
    sha1 = models.CharField(max_length=100) # TODO add unique
    add = models.IntegerField()
    sub = models.IntegerField()
    churn = models.IntegerField()
    char_add = models.IntegerField()
    char_sub = models.IntegerField()
    char_churn = models.IntegerField()
    merge = models.BooleanField()
    @classmethod
    def load_commits(cls, repository):
        raise NotImplementedError()

    def __repr__(self):
        return "< {sha1} - {repo} - {who}>".format(sha1=self.sha1, repo=self.repository.url, who=self.commiter.email)

    def __str__(self):
        return self.__repr__()


class CommitErrorType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __repr__(self):
        return "< {} >".format(self.name)

    def __str__(self):
        return self.__repr__()

class Submodule(models.Model):
    url = models.CharField(max_length=256)
    holder = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="holder_repository")
    dependency = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True,
                                   related_name="dependency_repository")

    def __repr__(self):
        return "< Submodule {0} of {1}>".format(self.url, self.holder.url)
        
    def __str__(self):
        return self.__repr__()


class PeriodChoice(Enum):
    LAST30 = "Last 30 days"
    LAST60 = "Last 60 days"
    LAST90 = "Last 90 days"
    LAST180 = "Last 180 days"
    LAST360 = "Last 360 days"


class CommitsMetrics(models.Model):
    add = models.IntegerField(default=0)
    sub = models.IntegerField(default=0)
    churn = models.IntegerField(default=0)
    char_add = models.IntegerField(default=0)
    char_sub = models.IntegerField(default=0)
    char_churn = models.IntegerField(default=0)
    merges = models.IntegerField(default=0)
    tags = models.IntegerField(default=0)
    repositories = models.IntegerField(default=0)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True)
    period = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in PeriodChoice]
    )

    @classmethod
    def max(cls):
        d = {}
        for period in PeriodChoice:
            all = [x.metrics for x in cls.objects.all()]
            d[str(period)] = {}
            for k in all[0].keys():
                d[str(period)][k] = []
            for entry in all:
                for k in all[0]:
                    d[str(period)][k].append(entry[k])
            for k in all[0]:
                d[str(period)][k] = max(d[str(period)][k])
        return d

    @classmethod
    def metrics_developer(cls, developer):
        d = {}
        for value in cls.objects.filter(commiter=developer):
            d[str(value.period)] = value.metrics
        return d

    @property
    def metrics(self):
        return dict(add=int(self.add),
                    sub=int(self.sub),
                    churn=int(self.churn),
                    merges=int(self.merges),
                    char_add=int(self.char_add),
                    char_sub=int(self.char_sub),
                    tags=int(self.tags),
                    repositories=int(self.repositories),
                    char_churn=int(self.char_churn))

    @classmethod
    def metrics_norm_developer(cls, developer):
        d = {}
        for value in cls.objects.filter(commiter=developer):
            k = list(filter(lambda v:str(value.period).__contains__(v.name),list(PeriodChoice)))[0].value
            d[k] = value.metrics_norm
        return d

    @property
    def metrics_norm(self):
        def norm_func(value, high):
            from math import log
            high = high if high != 0 else 1
            return log(1 + (value/high)*100)

        high = self.max()[self.period]
        values =  dict(add=self.add,
                    sub=self.sub,
                    churn=self.churn,
                    merges=self.merges,
                    char_add=self.char_add,
                    tags=self.tags,
                    repositories=self.repositories,
                    char_sub=self.char_sub,
                    char_churn=self.char_churn)
        for k,v in values.items():
            values[k] = norm_func(v, high[k])
        return values

    def __repr__(self):
        return "< {period} - {commiter} - {repo} >".format(period=self.period, commiter=self.commiter.email,
                                                           repo=self.repo.url if self.repo else "None")

    def __str__(self):
        return self.__repr__()


class Tag(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256, null=True)
    message = models.CharField(max_length=256, null=True)