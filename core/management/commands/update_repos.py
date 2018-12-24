from core.models import Repository
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        for repo in Repository.objects.all():
            print(repo)
            repo.update()