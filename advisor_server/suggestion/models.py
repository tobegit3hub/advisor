# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Study(models.Model):
  name = models.CharField(max_length=128, blank=False)
  study_configuration = models.TextField(blank=False)
  algorithm = models.CharField(max_length=128, blank=False)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}-{}".format(self.id, self.name)

  @classmethod
  def create(cls, name, study_configuration, algorithm="RandomSearchAlgorithm", status="PENDING"):
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
  study_id = models.IntegerField(blank=False)
  name = models.CharField(max_length=128, blank=False)
  parameter_values = models.TextField(blank=True, null=True)
  objective_value = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}-{}".format(self.id, self.name)

  @classmethod
  def create(cls, study_id, name):
    trial = cls()
    trial.study_id = study_id
    trial.name = name
    trial.status = "PENDING"
    trial.save()
    return trial

  def to_json(self):
    return {
        "id": self.id,
        "study_id": self.study_id,
        "name": self.name,
        "parameter_values": self.parameter_values,
        "objective_value": self.objective_value,
        "status": self.status,
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
    algorithm.save()
    return algorithm

  def as_json(self):
    return {"name": self.name}
