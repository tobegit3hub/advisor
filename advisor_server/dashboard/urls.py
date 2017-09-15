from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^studies$', views.studies, name='studies'),
    url(r'^studies/(?P<study_id>[\w.-]+)$', views.study, name='study'),
    url(r'^studies/(?P<study_id>[\w.-]+)/trials$', views.trials,
        name='trials'),
    url(r'^studies/(?P<study_id>[\w.-]+)/trials/(?P<trial_id>[\w.-]+)$',
        views.trial,
        name='trial'),
]
