from django.conf.urls import url
from . import views

urlpatterns = [
  url(r"^$", views.index, name="index"),
  #url(r"^v1/train$", views.v1_trains, name="v1_trains"),
]
