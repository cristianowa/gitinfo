from django.contrib import admin
from core.models import Commit, Submodule, CommitErrorType, Commiter, Repository, CommitsMetrics, Tag
# Register your models here.

admin.site.register(Commit)
admin.site.register(Commiter)
admin.site.register(Repository)

admin.site.register(CommitErrorType)
admin.site.register(Submodule)
admin.site.register(CommitsMetrics)
admin.site.register(Tag)