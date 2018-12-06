from django.contrib import admin
from core.models import Commit, Commiter, Repository
# Register your models here.

admin.site.register(Commit)
admin.site.register(Commiter)
admin.site.register(Repository)

