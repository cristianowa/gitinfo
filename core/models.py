import os
from enum import Enum

from django.db import models
import re

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


class CommitList(list):
    @property
    def sum(self):
        return sum([commit.add for commit in self])

    @property
    def sub(self):
        return sum([commit.sub for commit in self])

    @property
    def churn(self):
        return sum([commit.churn for commit in self])

    @property
    def char_sum(self):
        return sum([commit.add for commit in self])

    @property
    def char_sub(self):
        return sum([commit.sub for commit in self])

    @property
    def char_churn(self):
        return sum([commit.churn for commit in self])

    @property
    def merges(self):
        return len(list(filter(lambda commit:commit.merge, self)))

    @property
    def metrics(self):
        return dict(sum=self.sum, sub=self.sub, churn=self.churn, merges=self.merges,
                    char_sum=self.char_sum, char_sub=self.char_sub, char_churn=self.char_churn)

class Repository(models.Model):
    url = models.CharField(max_length=256, unique=True)

    def update(self):
        from gitinfo import cmd
        import shutil
        import gitinfo
        import tempfile
        tmp = tempfile.mkdtemp()
        cmd("git clone {0} {1}".format(self.url, tmp))
        commits = gitinfo.Commits()
        commits.load_commits(tmp)
        oldwd = os.getcwd()
        os.chdir(tmp)
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



        os.chdir(oldwd)
        shutil.rmtree(tmp, ignore_errors=True)

    def __repr__(self):
        return "< {url} >".format(url=self.url)

    def __str__(self):
        return self.__repr__()

    @property
    def commits(self):
        return CommitList(Commit.objects.filter(repository=self))

    def filter_commits(self, **kwargs):
        return CommitList(Commit.objects.filter(repository=self, **kwargs))



class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    date = models.DateTimeField(default="1990-01-01 09:30")
    sha1 = models.CharField(max_length=100)
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
    sum = models.IntegerField(default=0)
    sub = models.IntegerField(default=0)
    churn = models.IntegerField(default=0)
    char_sum = models.IntegerField(default=0)
    char_sub = models.IntegerField(default=0)
    char_churn = models.IntegerField(default=0)
    merges = models.IntegerField(default=0)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True)
    period = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in PeriodChoice]
    )


    @property
    def metrics(self):
        return dict(sum=int(self.sum),
                    sub=int(self.sub),
                    churn=int(self.churn),
                    merges=int(self.merges),
                    char_sum=int(self.char_sum),
                    char_sub=int(self.char_sub),
                    char_churn=int(self.char_churn))