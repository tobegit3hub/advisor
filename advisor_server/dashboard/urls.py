from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^v1/studies$', views.v1_studies, name='v1_studies'),
    url(r'^v1/studies/(?P<study_id>[\w.-]+)$', views.v1_study,
        name='v1_study'),
    url(r'^v1/trials$', views.v1_trials, name='v1_trials'),
    url(r'^v1/trials/(?P<trial_id>[\w.-]+)$', views.v1_trial, name='v1_trial'),
]
