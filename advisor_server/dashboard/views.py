# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


def index(request):
  context = {}
  return render(request, "index.html", context)


def studies(request):
  context = {}
  return render(request, "index.html", context)


def study(request, study_id):
  context = {}
  return render(request, "index.html", context)


def trials(request, study_id):
  context = {}
  return render(request, "index.html", context)


def trial(request, study_id, trial_id):
  context = {}
  return render(request, "index.html", context)
