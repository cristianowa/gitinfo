from django.db import models

# Create your models here.


class Commiter(models.Model):
    email = models.CharField(max_length=100)


class Repository(models.Model):
    url = models.CharField(max_length=256)


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    sha1 = models.CharField(max_length=100)
    add = models.IntegerField()
    sub = models.IntegerField()
    churn = models.IntegerField
    @classmethod
    def load_commits(cls, repository):
        raise NotImplementedError()

