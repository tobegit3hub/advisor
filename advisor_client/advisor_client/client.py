import os
import json
import requests

from .model import Study
from .model import Trial
from .model import TrialMetric


class AdvisorClient(object):
  def __init__(self, endpoint=None):
    # TODO: Read endpoint from configuration file
    if endpoint != None:
      self.endpoint = endpoint

    elif "ADVISOR_ENDPOINT" in os.environ:
      self.endpoint = os.environ.get("ADVISOR_ENDPOINT")

    else:
      self.endpoint = "http://0.0.0.0:8000"

  def create_study(self,
                   study_name,
                   study_configuration,
                   algorithm="BayesianOptimization"):
    url = "{}/suggestion/v1/studies".format(self.endpoint)
    request_data = {
        "name": study_name,
        "study_configuration": study_configuration,
        "algorithm": algorithm
    }
    response = requests.post(url, json=request_data)

    study = None
    if response.ok:
      study = Study.from_dict(response.json()["data"])

    return study

  def get_or_create_study(self,
                          study_name,
                          study_configuration,
                          algorithm="BayesianOptimization"):

    url = "{}/suggestion/v1/studies/{}/exist".format(self.endpoint, study_name)
    response = requests.get(url)
    study_exist = response.json()["exist"]

    if study_exist == True:
      study = self.get_study_by_name(study_name)
    else:
      study = self.create_study(study_name, study_configuration, algorithm)

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
  def get_study_by_name(self, study_name):
    url = "{}/suggestion/v1/studies/{}".format(self.endpoint, study_name)
    response = requests.get(url)
    study = None

    if response.ok:
      study = Study.from_dict(response.json()["data"])

    return study

  def get_suggestions(self, study_name, trials_number=1):
    url = "{}/suggestion/v1/studies/{}/suggestions".format(
        self.endpoint, study_name)
    request_data = {"trials_number": trials_number}
    response = requests.post(url, json=request_data)
    trials = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial = Trial.from_dict(dict)
        trials.append(trial)

    return trials

  def is_study_done(self, study_name):
    study = self.get_study_by_name(study_name)
    is_completed = True

    if study.status == "Completed":
      return True

    trials = self.list_trials(study_name)
    for trial in trials:
      if trial.status != "Completed":
        return False

    url = "{}/suggestion/v1/studies/{}".format(self.endpoint, trial.study_name)
    request_data = {"status": "Completed"}
    response = requests.put(url, json=request_data)

    return is_completed

  def list_trials(self, study_name):
    url = "{}/suggestion/v1/studies/{}/trials".format(self.endpoint,
                                                      study_name)
    response = requests.get(url)
    trials = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial = Trial.from_dict(dict)
        trials.append(trial)

    return trials

  def list_trial_metrics(self, study_name, trial_id):
    url = "{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        self.endpoint, study_name)
    response = requests.get(url)
    trial_metrics = []

    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial_metric = TrialMetric.from_dict(dict)
        trial_metrics.append(trial_metric)

    return trial_metrics

  def get_best_trial(self, study_name):
    if not self.is_study_done:
      return None

    study = self.get_study_by_name(study_name)
    study_configuration_dict = json.loads(study.study_configuration)
    study_goal = study_configuration_dict["goal"]
    trials = self.list_trials(study_name)

    best_trial = None
    best_objective_value = None

    # Get the first not null trial
    for trial in trials:
      if trial.objective_value:
        best_objective_value = trial.objective_value
        best_trial = trial
        break

    if best_trial == None:
      return None

    for trial in trials:
      if study_goal == "MAXIMIZE":
        if trial.objective_value and trial.objective_value > best_objective_value:
          best_trial = trial
          best_objective_value = trial.objective_value
      elif study_goal == "MINIMIZE":
        if trial.objective_value and trial.objective_value < best_objective_value:
          best_trial = trial
          best_objective_value = trial.objective_value
      else:
        return None

    return best_trial

  def get_trial(self, study_name, trial_id):
    url = "{}/suggestion/v1/studies/{}/trials/{}".format(
        self.endpoint, study_name, trial_id)
    response = requests.get(url)
    trial = None

    if response.ok:
      trial = Trial.from_dict(response.json()["data"])

    return trial

  def create_trial_metric(self, study_name, trial_id, training_step,
                          objective_value):
    url = "{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        self.endpoint, study_name, trial_id)
    request_data = {
        "training_step": training_step,
        "objective_value": objective_value
    }
    response = requests.post(url, json=request_data)

    study = None
    if response.ok:
      trial_metric = TrialMetric.from_dict(response.json()["data"])

    return trial_metric

  def complete_trial_with_tensorboard_metrics(self, trial,
                                              tensorboard_metrics):
    for tensorboard_metric in tensorboard_metrics:
      self.create_trial_metric(trial.study_name, trial.id,
                               tensorboard_metric.step,
                               tensorboard_metric.value)

    url = "{}/suggestion/v1/studies/{}/trials/{}".format(
        self.endpoint, trial.study_name, trial.id)
    objective_value = tensorboard_metrics[-1].value
    request_data = {"status": "Completed", "objective_value": objective_value}

    response = requests.put(url, json=request_data)

    if response.ok:
      trial = Trial.from_dict(response.json()["data"])

    return trial

  def complete_trial_with_one_metric(self, trial, metric):
    self.create_trial_metric(trial.study_name, trial.id, None, metric)

    url = "{}/suggestion/v1/studies/{}/trials/{}".format(
        self.endpoint, trial.study_name, trial.id)
    objective_value = metric
    request_data = {"status": "Completed", "objective_value": objective_value}

    response = requests.put(url, json=request_data)

    if response.ok:
      trial = Trial.from_dict(response.json()["data"])

    return trial
