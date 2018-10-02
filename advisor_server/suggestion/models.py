# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Study(models.Model):
  name = models.CharField(max_length=128, blank=False, unique=True)
  study_configuration = models.TextField(blank=False)
  algorithm = models.CharField(max_length=128, blank=False)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}-{}".format(self.id, self.name)

  @classmethod
  def create(cls,
             name,
             study_configuration,
             algorithm="RandomSearchAlgorithm",
             status="Pending"):
    study = cls()
    study.name = name
    study.study_configuration = study_configuration
    study.algorithm = algorithm
    study.status = status
    study.save()
    return study

  def to_json(self):
    return {
        "id": self.id,
        "name": self.name,
        "study_configuration": self.study_configuration,
        "algorithm": self.algorithm,
        "status": self.status,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }


class Trial(models.Model):
  # TODO: Use foreign key or not
  #study_name = models.ForeignKey(Study, related_name="trial_study", to_field=Study.name)
  study_name = models.CharField(max_length=128, blank=False)
  name = models.CharField(max_length=128, blank=False)
  parameter_values = models.TextField(blank=True, null=True)
  objective_value = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}-{}".format(self.id, self.name)

  @classmethod
  def create(cls, study_name, name):
    trial = cls()
    trial.study_name = study_name
    trial.name = name
    trial.status = "Pending"
    trial.save()
    return trial

  def to_json(self):
    return {
        "id": self.id,
        "study_name": self.study_name,
        "name": self.name,
        "parameter_values": self.parameter_values,
        "objective_value": self.objective_value,
        "status": self.status,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }


class TrialMetric(models.Model):
  trial_id = models.IntegerField(blank=False)
  training_step = models.IntegerField(blank=True, null=True)
  objective_value = models.FloatField(blank=True, null=True)

  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "Id: {}, trial id: {}, training_step: {}".format(
        self.id, self.trial_id, self.training_step)

  @classmethod
  def create(cls, trial_id, training_step, objective_value):
    trial_metric = cls()
    trial_metric.trial_id = trial_id
    trial_metric.training_step = training_step
    trial_metric.objective_value = objective_value
    trial_metric.save()
    return trial_metric

  def to_json(self):
    return {
        "id": self.id,
        "trial_id": self.trial_id,
        "training_step": self.training_step,
        "objective_value": self.objective_value,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }


class Algorithm(models.Model):
  name = models.CharField(max_length=128, blank=False)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}-{}".format(self.id, self.name)

  @classmethod
  def create(cls, name):
    algorithm = cls()
    algorithm.name = name
    algorithm.status = "AVAIABLE"
    algorithm.save()
    return algorithm

  def to_json(self):
    return {"name": self.name}
