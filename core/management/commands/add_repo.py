import traceback

from core.models import Repository, Commiter, CommitsMetrics
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        url = options["url"]
        branch = options["branch"] or "master"
        repo = Repository(url=url, branch=branch)
        repo.save()
        if not options["import_only"]:
            repo.update()

    def add_arguments(self, parser):
        parser.add_argument('url')
        parser.add_argument('--branch', default=None)
        parser.add_argument('--import-only', action='store_true', default=False)
