from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.main),

    url(r'^repository/(?P<pk>[0-9]+)/$', views.repository),
    url(r'^repository/(?P<pk>[0-9]+)/timeline.csv', views.repository_timeline_csv),
    url(r'^repository/(?P<pk>[0-9]+)/timeline.png', views.repository_timeline_graph),
    url(r'^graph/(?P<draw>[a-z]+)/(?P<type>[a-z]+)/', views.graph),
    url(r'^repository/add/', views.add_repository),
    url(r'^submodules/$', views.submodules),
    url(r'^submodules/graph/', views.submodule_dependency_graph),
    url(r'^developers/', views.developers),
    url(r'^developer/(?P<pk>[0-9]+)/$', views.developer),
    url(r'^developer/(?P<pk>[0-9]+)/(?P<days>[0-9al]+)/radar.png', views.developer_radar),
    url(r'^developer/(?P<pk>[0-9]+)/info.csv', views.developer_csv),
    url(r'^sshkey/', views.sshkey),
    url(r"^api/dump/", views.dump),
    url(r'^api/repository/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteRepository.as_view()),
    url(r'^api/commit/$', views.CommitList.as_view()),
    url(r'^api/commit/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommit.as_view()),
    url(r'^api/repository/$', views.RepositoryList.as_view()),
    url(r'^api/repository/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteRepository.as_view()),
    url(r'^api/repository/(?P<pk>[0-9]+)/update/', views.update_repository),
    url(r'^api/submodule/$', views.SubmoduleList.as_view()),
    url(r'^api/submodule/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteSubmodule.as_view()),
    url(r'^api/commiterrortype/$', views.CommiterrortypeList.as_view()),
    url(r'^api/commiterrortype/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommiterrortype.as_view()),
    url(r'^api/commitsmetrics/$', views.CommitsMetricsList.as_view()),
    url(r'^api/commitsmetrics/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommitsMetrics.as_view()),
]