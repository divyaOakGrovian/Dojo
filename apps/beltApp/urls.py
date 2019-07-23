from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^newJob$', views.newJob),
    url(r'^createJob$', views.createJob),
    url(r'^removeJob/(?P<job_id>\d+)$', views.removeJob),
    url(r'^dashboard/(?P<job_id>\d+)$', views.jobDetail),
    url(r'^editJob/(?P<job_id>\d+)$', views.editJob),
    url(r'^submitEditJob/(?P<job_id>\d+)$', views.submitEditJob),
    url(r'^addJob/(?P<job_id>\d+)$', views.addJob),
    url(r'^dropJob/(?P<job_id>\d+)$', views.dropJob),
]