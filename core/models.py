import os
from django.db import models

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
        os.chdir(oldwd)
        shutil.rmtree(tmp, ignore_errors=True)

    def __repr__(self):
        return "< {url} >".format(url=self.url)

    def __str__(self):
        return self.__repr__()

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