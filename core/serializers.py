from rest_framework import serializers
from core.models import Commit, Submodule, CommitErrorType, Repository, Commiter

class CommiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commiter
        fields = ('id', 'email',)

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('id', 'sha1', 'commiter', 'add', 'sub', 'churn',)

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


    