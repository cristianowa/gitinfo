from django.shortcuts import render
from .serializers import CommitSerializer, RepositorySerializer
from .models import Commit, Repository, Commiter
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
# Create your views here.


class CommitList(generics.ListCreateAPIView):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = CommitSerializer.Meta.fields

class GetUpdateDeleteCommit(generics.RetrieveUpdateDestroyAPIView):
    model = Commit
    serializer_class = CommitSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = CommitSerializer.Meta.fields


 
class RepositoryList(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = RepositorySerializer.Meta.fields


class GetUpdateDeleteRepository(generics.RetrieveUpdateDestroyAPIView):
    model = Repository
    serializer_class = RepositorySerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = RepositorySerializer.Meta.fields

@api_view(["POST"])
def update_repository(request, pk, *args, **kwargs):
    repository = Repository.objects.get(id=pk)
    repository.update()
    return JsonResponse({})


#TODO list/create ssh pub key so user can add it as deploy key to git