from rest_framework import serializers
from core.models import Commit, CommitErrorType, Repository, Commiter

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('id', 'sha1', 'commiter', 'add', 'sub', 'churn',)

class RepositorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Repository
            fields = ('id', 'url',)
        
    
class CommitErrorTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = CommitErrorType
            fields = ('name',)


    