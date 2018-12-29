from core.models import Repository, Commit
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        Commit.objects.all().delete()
        for repo in Repository.objects.all():
            print(repo)
            repo.update()