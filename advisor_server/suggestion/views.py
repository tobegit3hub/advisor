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
    studies = Study.objects.all()
    response_data = [study.to_json() for study in studies]
    return JsonResponse({"data": response_data})
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study(request, study_id):

  # Describe the study
  if request.method == "GET":
    study = Study.objects.get(id=study_id)
    return JsonResponse({"data": study.to_json()})

  # Update the study
  elif request.method == "PATCH":
    study = Study.objects.get(id=study_id)
    data = json.loads(request.body)
    if "status" in data:
      study.status = data["status"]
    study.save()
    return JsonResponse({"data": study.to_json()})

  # Delete the study
  elif request.method == "DELETE":
    study = Study.objects.get(id=study_id)
    study.delete()
    return JsonResponse({"message": "Success to delete"})
  else:
    return JsonResponse({"error": "Unsupported http method"})


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
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial(request, study_id, trial_id):

  # Describe the trial
  if request.method == "GET":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    return JsonResponse({"data": trial.to_json()})

  # Update the trial
  elif request.method == "PATCH":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    data = json.loads(request.body)
    if "status" in data:
      trial.status = data["status"]
    trial.save()
    return JsonResponse({"data": trial.to_json()})

  # Delete the trial
  elif request.method == "DELETE":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    trial.delete()
    return JsonResponse({"message": "Success to delete"})
  else:
    return JsonResponse({"error": "Unsupported http method"})
