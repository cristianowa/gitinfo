from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.main),

    url(r'^sshkey/', views.ssh_key),
    url(r'^repository/$', views.RepositoryList.as_view()),
    url(r'^graph/(?P<draw>[a-z]+)/(?P<type>[a-z]+)/', views.graph),
    url(r'^repository/add/', views.add_repository),
    url(r"^api/dump/", views.dump),
    url(r'^/api/repository/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteRepository.as_view()),
    url(r'^/api/commit/$', views.CommitList.as_view()),
    url(r'^/api/commit/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommit.as_view()),
    url(r'^/api/repository/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteRepository.as_view()),
    url(r'^/api/repository/(?P<pk>[0-9]+)/update/', views.update_repository),
    url(r'^/api/submodule/$', views.SubmoduleList.as_view()),
    url(r'^/api/submodule/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteSubmodule.as_view()),
    url(r'^/api/commiterrortype/$', views.CommiterrortypeList.as_view()),
    url(r'^/api/commiterrortype/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommiterrortype.as_view()),
]