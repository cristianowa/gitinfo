from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
import pandas as pd
from .graphs import get_graph
from .models import Commiter, Submodule, Commit, CommitErrorType, Repository, CommitsMetrics
from .serializers import CommiterSerializer, SubmoduleSerializer, CommitSerializer, CommitErrorTypeSerializer,\
    RepositorySerializer, commits_serializer, CommitsMetricsSerializer
from .forms import NewRepository

# Create your views here.

# Rest API

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


class CommitsMetricsList(generics.ListCreateAPIView):
    queryset = CommitsMetrics.objects.all()
    serializer_class = SubmoduleSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = SubmoduleSerializer.Meta.fields


class GetUpdateDeleteCommitsMetrics(generics.RetrieveUpdateDestroyAPIView):
    model = CommitsMetrics
    serializer_class = CommitsMetricsSerializer
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


@api_view(["GET"])
def dump(request):
    return JsonResponse(dump_data())


def view_all(request):
    data = dump_data()
    render(request, "view_all.html", data)


# Graphs view

def graph(request, draw, type):
    repository = Repository.objects.get(url=request.GET["repository"])
    days = request.GET.get("days") or 30
    return render(request, "graph.html", {"chart": get_graph(repository, days, type, draw)})

# HTML views

def main(request):
    repos = Repository.objects.all()
    repos = [dict(name=r.url, url=r.url) for r in repos]
    return render(request, "main.html", dict(repos=repos))

def sshkey(request):
    import sys, os
    if "win" in sys.platform.lower():
        sshkey = open(os.path.join(os.environ.get("HOMEPATH"), ".ssh/id_rsa.pub")).read()
    else:
        sshkey = open(os.path.join(os.environ.get("HOME"), ".ssh/id_rsa.pub")).read()

    return render(request, "ssh_key.html", dict(sshkey=sshkey))

def developers(request):
    from . models import Commiter
    commiters = [dict(id=c.id, email=c.email) for c in Commiter.objects.all()]
    return render(request, "developers.html", dict(commiters=commiters))


def developer(request, pk):
    from .models import Commiter, CommitsMetrics
    commiter = Commiter.objects.get(id=pk)
    metrics = CommitsMetrics.metrics_developer(commiter)
    return render(request, "developer.html", dict(commiter=commiter, metrics=metrics, metrics_names=[''] + list(list(metrics.values())[0].keys())))


def developer_radar(request, pk, days):
    from .models import Commiter, CommitsMetrics
    from .graphs import radar_plot
    import tempfile
    tmp = tempfile.mktemp(".png")
    commiter = Commiter.objects.get(id=pk)
    raw_metrics = CommitsMetrics.metrics_norm_developer(commiter)
    if days=="all":
        # metrics = {}
        labels= list(raw_metrics.keys())
        # for day in raw_metrics.keys():
        #     for k in raw_metrics[list(raw_metrics.keys())[0]].keys():
        #         metrics[k].append(raw_metrics[day][k])
        metrics = list(raw_metrics.values())
    else:
        metrics = raw_metrics["PeriodChoice.LAST{}".format(days)]
        labels = [days]
    radar_plot(tmp, metrics, labels=labels)
    with open(tmp, "rb") as f:
        bytes = f.read()
    return HttpResponse(bytes, content_type="image/png")

def developer_csv(request, pk):
    import csv
    # Create the HttpResponse object with the appropriate CSV header.
    dev = Commiter.objects.get(id=pk)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(dev.email)

    report = dev.report
    response.write("\nMetrics\n")
    response.write(pd.DataFrame.from_dict(report["metrics"]).to_csv())
    response.write("\nMetrics Normalized\n")
    response.write(pd.DataFrame.from_dict(report["metrics_normalized"]).to_csv())
    response.write("\nRepositories\n")
    response.write(pd.DataFrame.from_dict(report["repositories"]).to_csv())

    return response


def repository(request, pk):
    from .models import Repository
    repo = Repository.objects.get(id=pk)
    return render(request, "repository.html", dict(repository=repo))

def submodules(request):
    from .models import Submodule
    submodules = Submodule.objects.all()
    return render(request, "submodules.html", dict())

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