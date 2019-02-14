from django.contrib import admin
from core.models import Commit, Submodule, CommitErrorType, Commiter, Repository, CommitsMetrics, Tag, \
    CommitBlamePercentage
# Register your models here.

class CommitAdmin(admin.ModelAdmin):
    search_fields = ["sha1", "commiter__email"]

admin.site.register(Commit, CommitAdmin)
class CommiterAdmin(admin.ModelAdmin):
    search_fields = ["email"]
admin.site.register(Commiter, CommiterAdmin)
class RepositoryAdmin(admin.ModelAdmin):
    search_fields = ["url"]
admin.site.register(Repository, RepositoryAdmin)

admin.site.register(CommitErrorType)
class RepositoryAdmin(admin.ModelAdmin):
    search_fields = ["url"]
admin.site.register(Submodule)
admin.site.register(CommitsMetrics)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["commit__sha", "commiter__email"]
admin.site.register(Tag, TagAdmin)
class CommitBlamePercentageAdmin(admin.ModelAdmin):
    search_fields = ["commit__sha1", "commiter__email", "commit__repository__url"]
admin.site.register(CommitBlamePercentage, CommitBlamePercentageAdmin)