import traceback

from core.models import Repository, Commiter, CommitsMetrics
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        for commiter in Commiter.objects.all():
            try:
                print(commiter)
                commiter.update()
            except Exception as e:
                print("===========> error")
                print(e)
                print(commiter)
                traceback.print_exc()


