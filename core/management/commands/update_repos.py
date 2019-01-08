from core.models import Repository, Commiter, CommitsMetrics
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        for repo in Repository.objects.all():
            print(repo)
            repo.update()
        for commiter in Commiter.objects.all():
            print(commiter)
            commiter.update()
