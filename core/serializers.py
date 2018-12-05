from rest_framework import serializers
from core.models import Commit

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('sha1', 'commiter', 'add', 'sub', 'churn')

