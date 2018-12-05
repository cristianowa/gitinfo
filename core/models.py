from django.db import models

# Create your models here.


class Commiter(models.Model):
    email = models.CharField(max_length=100)


class Commit(models.Model):
    commiter = models.ForeignKey(Commiter, on_delete=models.CASCADE)
    sha1 = models.CharField(max_length=100)
    add = models.IntegerField()
    sub = models.IntegerField()
    churn = models.IntegerField
    @classmethod
    def load_commits(cls):
        raise NotImplementedError()



