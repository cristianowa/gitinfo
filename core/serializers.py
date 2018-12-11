from rest_framework import serializers
from core.models import Commit, Repository, Commiter

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('id', 'sha1', 'commiter', 'add', 'sub', 'churn',)

class RepositorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Repository
            fields = ('id', 'url',)
        
    
