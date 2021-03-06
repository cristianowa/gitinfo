from rest_framework import serializers
from core.models import Commit, Submodule, CommitErrorType, Repository, Commiter, CommitsMetrics

class CommiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commiter
        fields = ('id', 'email',)

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('id', 'sha1', 'commiter', 'add', 'sub', 'churn','date',
                  'char_add', 'char_sub', 'char_churn', 'merge')

class RepositorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Repository
            fields = ('id', 'url',)


def commits_serializer(commits):
    data = []
    for commit in commits:
        data.append(CommitSerializer(commit).data)
    return data
    
class CommitErrorTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = CommitErrorType
            fields = ('name',)


class SubmoduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submodule
        fields = ('url','holder','dependency')


class CommitsMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitsMetrics
        fields = ('id','sub', 'add',' churn', 'merges', 'char_add', 'char_churn', 'char_sub')
