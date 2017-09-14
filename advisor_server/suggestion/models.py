# -*- coding: utf-8 -*-

from django.db import models


class Study(models.Model):
  name = models.CharField(max_length=128, blank=False)

  def __str__(self):
    return "{}-{}".format(self.org_id, self.job_name)

  @classmethod
  def create(cls, name):
    study = cls()
    study.name = name

  def as_json(self):
    return {"name": self.name}


class Trial(models.Model):
  name = models.CharField(max_length=128, blank=False)

  def __str__(self):
      return "{}-{}".format(self.org_id, self.job_name)

  @classmethod
  def create(cls, name):
      trial = cls()
      trial.name = name

  def as_json(self):
      return {"name": self.name}
