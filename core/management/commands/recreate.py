from core.models import Repository, Commit, Commiter, CommitsMetrics
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        Commit.objects.all().delete()
        Commiter.objects.all().delete()
        CommitsMetrics.objects.all().delete()
        for repo in Repository.objects.all():
            print(repo)
            repo.update()
        for commiter in Commiter.objects.all():
            print(commiter)
            commiter.update()