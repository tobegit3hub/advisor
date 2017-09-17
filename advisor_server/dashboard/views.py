# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
import platform

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django import forms
from django.contrib.admin.views.decorators import staff_member_required

from suggestion.models import Study
from suggestion.models import Trial


def index(request):
  try:
    studies = [study.to_json() for study in Study.objects.all()]
  except Study.DoesNotExist:
    studies = []

  try:
    trials = [trial.to_json() for trial in Trial.objects.all()]
  except Study.DoesNotExist:
    trials = []

  context = {
      "success": True,
      "studies": studies,
      "trials": trials,
      "platform": platform
  }
  return render(request, "index.html", context)


@csrf_exempt
def v1_studies(request):
  if request.method == "POST":
    name = request.POST.get("name", "")
    study_configuration = request.POST.get("study_configuration", "")

    # Remove the charactors like \t and \"
    study_configuration_json = json.loads(study_configuration)
    data = {"name": name, "study_configuration": study_configuration_json}

    url = "http://127.0.0.1:8000/suggestion/v1/studies"
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return redirect("index")
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)


@csrf_exempt
def v1_study(request, study_id):
  url = "http://127.0.0.1:8000/suggestion/v1/studies/{}".format(study_id)

  if request.method == "GET":
    response = requests.get(url)

    tirals_url = "http://127.0.0.1:8000/suggestion/v1/studies/{}/trials".format(
        study_id)
    tirals_response = requests.get(tirals_url)

    if response.ok and tirals_response.ok:
      study = json.loads(response.content.decode("utf-8"))["data"]
      trials = json.loads(tirals_response.content.decode("utf-8"))["data"]
      context = {"success": True, "study": study, "trials": trials}
      return render(request, "study_detail.html", context)
    else:
      response = {
          "error": True,
          "message": "Fail to request the url: {}".format(url)
      }
      return JsonResponse(response, status=405)
  elif request.method == "DELETE" or request.method == "POST":
    response = requests.delete(url)
    messages.info(request, response.content)
    return redirect("index")
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)


@csrf_exempt
def v1_study_suggestions(request, study_id):
  if request.method == "POST":
    trials_number_string = request.POST.get("trials_number", "1")
    trials_number = int(trials_number_string)

    data = {"trials_number": trials_number}
    url = "http://127.0.0.1:8000/suggestion/v1/studies/{}/suggestions".format(
        study_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trials(request):
  if request.method == "POST":
    study_id = request.POST.get("study_id", "")
    name = request.POST.get("name", "")

    data = {"name": name}

    url = "http://127.0.0.1:8000/suggestion/v1/studies/{}/trials".format(
        study_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return redirect("index")
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial(request, study_id, trial_id):
  url = "http://127.0.0.1:8000/suggestion/v1/studies/{}/trials/{}".format(
      study_id, trial_id)

  if request.method == "GET":
    response = requests.get(url)
    if response.ok:
      trial = json.loads(response.content.decode("utf-8"))["data"]
      context = {"success": True, "trial": trial}
      return render(request, "trial_detail.html", context)
    else:
      response = {
          "error": True,
          "message": "Fail to request the url: {}".format(url)
      }
      return JsonResponse(response, status=405)
  elif request.method == "DELETE" or request.method == "POST":
    response = requests.delete(url)
    messages.info(request, response.content)
    return redirect("index")
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)
