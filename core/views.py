from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from graphos.renderers import yui
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from core.datasource import CommitsByDeveloper, CommitsByDeveloperLog
from .models import Commiter, Submodule, Commit, CommitErrorType, Repository
from .serializers import CommiterSerializer, SubmoduleSerializer, CommitSerializer, CommitErrorTypeSerializer,\
    RepositorySerializer, commits_serializer
from .forms import NewRepository

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

# Rest API

class CommiterrortypeList(generics.ListCreateAPIView):
    queryset = CommitErrorType.objects.all()
    serializer_class = CommitErrorTypeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = CommitErrorTypeSerializer.Meta.fields


class GetUpdateDeleteCommiterrortype(generics.RetrieveUpdateDestroyAPIView):
    model = CommitErrorType
    serializer_class = CommitErrorTypeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = CommitErrorTypeSerializer.Meta.fields


class SubmoduleList(generics.ListCreateAPIView):
    queryset = Submodule.objects.all()
    serializer_class = SubmoduleSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = SubmoduleSerializer.Meta.fields


class GetUpdateDeleteSubmodule(generics.RetrieveUpdateDestroyAPIView):
    model = Submodule
    serializer_class = SubmoduleSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = SubmoduleSerializer.Meta.fields

 
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


def dump_data():
    data = {"repositories" : {}, "commiters": {}}
    for commiter in Commiter.objects.all():
        data["commiters"][str(commiter.email)] = {"info": CommiterSerializer(commiter).data}
        data["commiters"][str(commiter.email)]["commits"] = []
        data["commiters"][str(commiter.email)]["repos"] = {}
    for repo in Repository.objects.all():
        repo_serializer = RepositorySerializer(repo)
        data["repositories"][str(repo.url)] = {"info": repo_serializer.data}
        data["repositories"][str(repo.url)] = {"commits": commits_serializer(repo.commits)}
        for commiter in Commiter.objects.all():
            commits = repo.filter_commits(commiter=commiter)
            data["commiters"][str(commiter.email)]["commits"] += commits_serializer(commits)
            data["commiters"][str(commiter.email)]["repos"][str(repo.url)] = commits_serializer(commits)
    return data

def view_all(request):
    data = dump_data()
    render(request, "view_all.html", data)

@api_view(["GET"])
def dump(request):
    return JsonResponse(dump_data())




# Graphs view

def get_graph(repository, days, type="log", draw="pie"):
    periodo_start = datetime.today() - timedelta(days=int(days))
    queryset = Commit.objects.filter(repository=repository, date__gte=periodo_start)
    type_function = {
        "log":CommitsByDeveloperLog,
        "normal":CommitsByDeveloper
    }
    datasource = type_function[type](queryset=queryset, fields=['commiter', 'add', 'sub', 'churn'])
    draw_function = {
        "bar": yui.BarChart,
        "pie": yui.PieChart
    }
    return draw_function[draw](datasource)

def graph(request, draw, type):
    from datetime import datetime, timedelta
    repository = Repository.objects.get(url=request.GET["repository"])
    days = request.GET.get("days") or 30
    return render(request, "graph.html", {"chart": get_graph(repository, days, type, draw)})

# HTML views

def main(request):
    repos = Repository.objects.all()
    repos = [dict(name=r.url, url=r.url) for r in repos]
    return render(request, "main.html", dict(repos=repos))

def ssh_key(request):
    import sys, os
    if "win" in sys.platform.lower():
        sshkey = open(os.path.join(os.environ.get("HOMEPATH"), ".ssh/id_rsa.pub")).read()
    else:
        sshkey = open(os.path.join(os.environ.get("HOME"), ".ssh/id_rsa.pub")).read()

    return render(request, "ssh_key.html", dict(sshkey=sshkey))


def add_repository(request):

    if request.method == 'POST':
        form = NewRepository(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            repo = Repository(url=url)
            repo.save()
            repo.update()
            repos = [dict(name=r.url,
                          pie_normal_url="/git/graph/pie/normal/?repository={}".format(r.url),
                          pie_log_url="/git/graph/pie/log/?repository={}".format(r.url),
                          bar_normal_url="/git/graph/bar/log/?repository={}".format(r.url),
                          bar_log_url="/git/graph/bar/log/?repository={}".format(r.url)) for r in [repo]]
            return render(request, "main.html", dict(repos=repos))
    else:
        form = NewRepository()

    return render(request, 'add_repository.html', {'form': form})