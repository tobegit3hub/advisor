from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^", views.index, name="index"),
    url(r"^v1/studies$", views.v1_studies, name="v1_studies"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)$", views.v1_study,
        name="v1_study"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/exist$", views.v1_study_exist,
        name="v1_study_exist"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/suggestions$",
        views.v1_study_suggestions,
        name="v1_study_suggestions"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/trials$",
        views.v1_study_trials,
        name="v1_study_trials"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/trials/(?P<trial_id>[\w.-]+)$",
        views.v1_study_trial,
        name="v1_study_trial"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/trials/(?P<trial_id>[\w.-]+)/metrics$",
        views.v1_study_trial_metrics,
        name="v1_study_trial_metrics"),
    url(r"^v1/studies/(?P<study_name>[\w.-]+)/trials/(?P<trial_id>[\w.-]+)/metrics/(?P<metric_id>[\w.-]+)$",
        views.v1_study_trial_metric,
        name="v1_study_trial_metric"),
]
