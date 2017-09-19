import json
import logging
import requests

from .model import Study
from .model import Trial
from .model import TrialMetric


class AdvisorClient(object):
  def __init__(self, endpoint="http://127.0.0.1:8000"):
    self.endpoint = endpoint

  def create_study(self, name, study_configuration):
    url = "{}/suggestion/v1/studies".format(self.endpoint)
    request_data = {"name": name, "study_configuration": study_configuration}
    response = requests.post(url, json=request_data)

    study = None
    if response.ok:
      study = Study.from_dict(response.json()["data"])

    return study

  def list_studies(self):
    url = "{}/suggestion/v1/studies".format(self.endpoint)
    response = requests.get(url)
    studies = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        study = Study.from_dict(dict)
        studies.append(study)

    return studies

  # TODO: Support load study by configuration and name
  def get_study(self, study_id):
    url = "{}/suggestion/v1/studies/{}".format(self.endpoint, study_id)
    response = requests.get(url)
    study = None

    if response.ok:
      study = Study.from_dict(response.json()["data"])

    return study

  # TODO: Implement this method by status's status
  def is_study_done(self):
    return False

  def get_suggestions(self, study_id, trials_number=1):
    url = "{}/suggestion/v1/studies/{}/suggestions".format(
        self.endpoint, study_id)
    request_data = {"trials_number": trials_number}
    response = requests.post(url, json=request_data)
    trials = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial = Trial.from_dict(dict)
        trials.append(trial)

    return trials

  def list_trials(self, study_id):
    url = "{}/suggestion/v1/studies/{}/trials".format(self.endpoint, study_id)
    response = requests.get(url)
    trials = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial = Trial.from_dict(dict)
        trials.append(trial)

    return trials

  def list_trial_metrics(self, study_id, trial_id):
    url = "{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        self.endpoint, study_id)
    response = requests.get(url)
    trial_metrics = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial_metric = TrialMetric.from_dict(dict)
        trial_metrics.append(trial_metric)

    return trial_metrics

  def create_trial_metric(self, study_id, trial_id, training_step,
                          objective_value):
    url = "{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        self.endpoint, study_id, trial_id)
    request_data = {
        "training_step": training_step,
        "objective_value": objective_value
    }
    response = requests.post(url, json=request_data)

    study = None
    if response.ok:
      trial_metric = TrialMetric.from_dict(response.json()["data"])

    return trial_metric

  def complete_trial(self, trial, tensorboard_metrics):
    for tensorboard_metric in tensorboard_metrics:
      self.create_trial_metric(trial.study_id, trial.id,
                               tensorboard_metric.step,
                               tensorboard_metric.value)

    url = "{}/suggestion/v1/studies/{}/trials/{}".format(
        self.endpoint, trial.study_id, trial.id)
    request_data = {"status": "SUCCESS"}
    response = requests.put(url, json=request_data)

    if response.ok:
      trial = Trial.from_dict(response.json()["data"])

    return trial
