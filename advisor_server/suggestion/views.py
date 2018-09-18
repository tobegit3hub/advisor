# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.models import TrialMetric
from suggestion.algorithm.random_search import RandomSearchAlgorithm
from suggestion.algorithm.grid_search import GridSearchAlgorithm
from suggestion.algorithm.bayesian_optimization import BayesianOptimization
from suggestion.algorithm.tpe import TpeAlgorithm


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
    algorithm = data.get("algorithm", "RandomSearchAlgorithm")

    study = Study.create(name, study_configuration, algorithm)
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
  elif request.method == "PUT":
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
def v1_study_suggestions(request, study_id):
  # Create the trial
  if request.method == "POST":
    data = json.loads(request.body)
    trials_number = 1
    trial_name = "Trial"
    if "trials_number" in data:
      trials_number = data["trials_number"]
    if "trial_name" in data:
      trial_name = data["trial_name"]

    study = Study.objects.get(id=study_id)
    trials = Trial.objects.filter(study_id=study_id)
    trials = [trial for trial in trials]

    if study.algorithm == "RandomSearchAlgorithm":
      algorithm = RandomSearchAlgorithm()
    elif study.algorithm == "GridSearchAlgorithm":
      algorithm = GridSearchAlgorithm()
    elif study.algorithm == "BayesianOptimization":
      algorithm = BayesianOptimization()
    elif study.algorithm == "TpeAlgorithm":
      algorithm = TpeAlgorithm()
    elif study.algorithm == "SimulateAnnealAlgorithm":
      algorithm = TpeAlgorithm()
    else:
      return JsonResponse({
          "error":
          "Unknown algorithm: {}".format(study.algorithm)
      })

    new_trials = algorithm.get_new_suggestions(study.id, trials, trials_number)

    return JsonResponse({"data": [trial.to_json() for trial in new_trials]})
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study_trials(request, study_id):

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
def v1_study_trial(request, study_id, trial_id):

  # Describe the trial
  if request.method == "GET":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    return JsonResponse({"data": trial.to_json()})

  # Update the trial
  elif request.method == "PUT":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    data = json.loads(request.body)
    if "status" in data:
      trial.status = data["status"]
    if "objective_value" in data:
      trial.objective_value = data["objective_value"]
    trial.save()
    return JsonResponse({"data": trial.to_json()})

  # Delete the trial
  elif request.method == "DELETE":
    trial = Trial.objects.get(study_id=study_id, id=trial_id)
    trial.delete()
    return JsonResponse({"message": "Success to delete"})
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study_trial_metrics(request, study_id, trial_id):

  # Create the trial metric
  if request.method == "POST":
    data = json.loads(request.body)
    training_step = data["training_step"]
    objective_value = data["objective_value"]

    trial_metric = TrialMetric.create(trial_id, training_step, objective_value)
    return JsonResponse({"data": trial_metric.to_json()})

  # List the trial metrics
  elif request.method == "GET":
    trial_metrics = TrialMetric.objects.filter(trial_id=trial_id)
    response_data = [trial_metric.to_json() for trial_metric in trial_metrics]
    return JsonResponse({"data": response_data})
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study_trial_metric(request, study_id, trial_id, metric_id):

  # Describe the trial metric
  if request.method == "GET":
    trial_metric = TrialMetric.objects.get(id=metric_id)
    return JsonResponse({"data": trial_metric.to_json()})

  # Update the trial metric
  elif request.method == "PATCH":
    trial_metric = TrialMetric.objects.get(id=metric_id)
    data = json.loads(request.body)
    if "training_step" in data:
      trial_metric.training_step = data["training_step"]
    if "objective_value" in data:
      trial_metric.objective_value = data["objective_value"]
    trial_metric.save()
    return JsonResponse({"data": trial_metric.to_json()})

  # Delete the trial metric
  elif request.method == "DELETE":
    trial_metric = TrialMetric.objects.get(id=metric_id)
    trial_metric.delete()
    return JsonResponse({"message": "Success to delete"})
  else:
    return JsonResponse({"error": "Unsupported http method"})
