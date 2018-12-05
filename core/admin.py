from django.contrib import admin
from core.models import Commit, Commiter
# Register your models here.

admin.site.register(Commit)
admin.site.register(Commiter)

