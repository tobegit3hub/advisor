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
        "randomInitTrials":
        1,
        "params": [{
            "parameterName": "hidden2",
            "type": "DISCRETE",
            "feasiblePoints": "8, 16, 32, 64",
            "scalingType": "LINEAR"
        }, {
            "parameterName": "optimizer",
            "type": "CATEGORICAL",
            "feasiblePoints": "sgd, adagrad, adam, ftrl",
            "scalingType": "LINEAR"
        }, {
            "parameterName": "batch_normalization",
            "type": "CATEGORICAL",
            "feasiblePoints": "true, false",
            "scalingType": "LINEAR"
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
        self.study.id, self.trials, 1)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 1)

  def test_get_two_new_suggestions(self):
    gridSearchAlgorithm = GridSearchAlgorithm()
    new_trials = gridSearchAlgorithm.get_new_suggestions(
        self.study.id, self.trials, 2)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 2)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertEqual(new_parameter_values_json["hidden2"], "8")
    self.assertEqual(new_parameter_values_json["optimizer"], "sgd")
    self.assertEqual(new_parameter_values_json["batch_normalization"], "true")
