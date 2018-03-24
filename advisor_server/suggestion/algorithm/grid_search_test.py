import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.grid_search import GridSearchAlgorithm


class GridSearchAlgorithmTest(TestCase):
  def setUp(self):
    study_configuration_json = {
        "goal":
        "MAXIMIZE",
        "maxTrials":
        5,
        "maxParallelTrials":
        1,
        "params": [{
            "parameterName": "hidden1",
            "type": "INTEGER",
            "minValue": 40,
            "maxValue": 400,
            "scallingType": "LINEAR"
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("GridSearchStudy", study_configuration)
    self.trials = []

  def tearDown(self):
    pass

  def test_init(self):
    gridSearchAlgorithm = GridSearchAlgorithm()
    self.assertEqual(gridSearchAlgorithm.__class__, GridSearchAlgorithm)

  def test_get_new_suggestions(self):
    gridSearchAlgorithm = GridSearchAlgorithm()
    new_trials = gridSearchAlgorithm.get_new_suggestions(
        self.study.id, self.trials, 2)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 2)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 40)

    new_trial = new_trials[1]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 400)

  def test_get_four_new_suggestions(self):
    gridSearchAlgorithm = GridSearchAlgorithm()
    new_trials = gridSearchAlgorithm.get_new_suggestions(
        self.study.id, self.trials, 4)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 4)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 40)

    new_trial = new_trials[1]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 160)

    new_trial = new_trials[2]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 280)

    new_trial = new_trials[3]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden1"], 400)
