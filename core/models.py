import os
from django.db import models
import re

# Create your models here.


class Commiter(models.Model):
    email = models.CharField(max_length=100, unique=True)
    def __repr__(self):
        return "< {email} >".format(email=self.email)

    def __str__(self):
        return self.__repr__()

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
                                  churn=commit.changes["churn"])
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
        return list(Commit.objects.filter(repository=self))

    def filter_commits(self, **kwargs):
        return list(Commit.objects.filter(repository=self, **kwargs))


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    date = models.DateTimeField(default="1990-01-01 09:30")
    sha1 = models.CharField(max_length=100)
    add = models.IntegerField()
    sub = models.IntegerField()
    churn = models.IntegerField()
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
