from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^commit/$', views.CommitList.as_view()),
    url(r'^commit/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteCommit.as_view()),
    url(r'^repository/$', views.RepositoryList.as_view()),
    url(r'^repository/(?P<pk>[0-9]+)/$', views.GetUpdateDeleteRepository.as_view()),
    url(r'^repository/(?P<pk>[0-9]+)/update/', views.update_repository)
]