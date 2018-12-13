from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from graphos.renderers import yui
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from core.datasource import CommitsByDeveloper, CommitsByDeveloperLog
from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer


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


def bar_graph(request, type):
    from datetime import datetime, timedelta
    repository = Repository.objects.get(url=request.GET["repository"])
    days = request.GET.get("days") or 30
    periodo_start = datetime.today() - timedelta(days=int(days))
    queryset = Commit.objects.filter(repository=repository, date__gte=periodo_start)
    if type == "log":
        datasource = CommitsByDeveloperLog(queryset=queryset, fields=['commiter', 'add', 'sub', 'churn'])
    else:
        datasource = CommitsByDeveloper(queryset=queryset, fields=['commiter', 'add', 'sub', 'churn'])
    chart = yui.BarChart(datasource)
    return render(request, "bar_graph.html",{"chart":chart})

#TODO list/create ssh pub key so user can add it as deploy key to git