import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.random_search import RandomSearchAlgorithm


class RandomSearchAlgorithmTest(TestCase):
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
            "parameterName": "hidden1",
            "type": "INTEGER",
            "minValue": 1,
            "maxValue": 10,
            "scalingType": "LINEAR"
        }, {
            "parameterName": "learning_rate",
            "type": "DOUBLE",
            "minValue": 0.01,
            "maxValue": 0.5,
            "scalingType": "LINEAR"
        }, {
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
    self.study = Study.create("RandomSearchStudy", study_configuration)

  def tearDown(self):
    pass

  def test_init(self):
    instance = RandomSearchAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, RandomSearchAlgorithm)

  def test_get_new_suggestions(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()

    new_trials = randomSearchAlgorithm.get_new_suggestions(
        self.study.id, number=1)
    new_trial = new_trials[0]
    new_parameter_values_json = json.loads(new_trial.parameter_values)

    self.assertTrue(10 >= new_parameter_values_json["hidden1"] >= 1)
    self.assertTrue(0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)
    self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
    self.assertTrue(new_parameter_values_json["optimizer"] in [
        "sgd", "adagrad", "adam", "ftrl"
    ])
    self.assertTrue(
        new_parameter_values_json["batch_normalization"] in ["true", "false"])

  def test_get_multiple_new_suggestions(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()

    # Assert getting one trial
    new_trials = randomSearchAlgorithm.get_new_suggestions(
        self.study.id, number=1)
    self.assertEqual(len(new_trials), 1)

    # Assert getting multiple trials
    new_trials = randomSearchAlgorithm.get_new_suggestions(
        self.study.id, number=10)
    self.assertEqual(len(new_trials), 10)
