# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError, transaction

from suggestion.models import Study
from suggestion.models import Trial

import json


def index(request):
  response = {"message": "Welcome to advisor"}
  return JsonResponse(response)


@csrf_exempt
def v1_studies(request):
  # Create the study
  if request.method == "POST":
    data = json.loads(request.body)
    name = data["name"]
    study_configuration = json.dumps(data["study_configuration"])

    study = Study.create(name, study_configuration)
    return JsonResponse({"data": study.to_json()})

  # List the studies
  elif request.method == "GET":
    pass

    studies = Study.objects.all()
    response_data = [study.to_json() for study in studies]
    return JsonResponse({"data": response_data})
  else:
    response = {"error": "Unsupported http method"}
    return JsonResponse(response)


@csrf_exempt
def v1_study(request, study_id):
  if request.method == "GET":
    pass
  elif request.method == "DELETE":
    pass

  response = {"study_id": study_id}
  return JsonResponse(response)


@csrf_exempt
def v1_trials(request, study_id):
  # Create the trial
  if request.method == "POST":
    data = json.loads(request.body)
    name = data["name"]

    trial = Trial.create(study_id, name)
    return JsonResponse({"data": trial.to_json()})

  # List the studies
  elif request.method == "GET":
    trials = Trial.objects.filter(study_id=study_id)
    response_data = [trial.to_json() for trial in trials]
    return JsonResponse({"data": response_data})
  else:
    response = {"error": "Unsupported http method"}
    return JsonResponse(response)


@csrf_exempt
def v1_trial(request, study_id, trial_id):
  if request.method == "GET":
    pass
  elif request.method == "DELETE":
    pass

  response = {"study_id": study_id, "trial_id": trial_id}
  return JsonResponse(response)
