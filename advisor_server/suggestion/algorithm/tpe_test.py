import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.tpe import TpeAlgorithm


class TpeAlgorithmTest(TestCase):
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
            "parameterName": "l1_normalization",
            "type": "DOUBLE",
            "minValue": 0.01,
            "maxValue": 0.99,
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
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("TpeStudy", study_configuration)

  def tearDown(self):
    pass

  def test_init(self):
    instance = TpeAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, TpeAlgorithm)

  def test_get_new_suggestions(self):
    tpeAlgorithm = TpeAlgorithm()

    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, number=1)
    new_trial = new_trials[0]
    new_parameter_values_json = json.loads(new_trial.parameter_values)

    self.assertTrue(
        0.99 >= new_parameter_values_json["l1_normalization"] >= 0.01)
    self.assertTrue(0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)
    self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
    self.assertTrue(new_parameter_values_json["optimizer"] in [
        "sgd", "adagrad", "adam", "ftrl"
    ])

  def test_get_multiple_new_suggestions(self):
    tpeAlgorithm = TpeAlgorithm()

    # Assert getting one trial
    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, number=1)
    self.assertEqual(len(new_trials), 1)

    # Assert getting multiple trials
    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, number=10)
    self.assertEqual(len(new_trials), 10)

  def test_complete_and_get_new_suggestions(self):
    tpeAlgorithm = TpeAlgorithm()

    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, [], 1)
    new_trials[0].status = "Completed"
    new_trials[0].objective_value = 0.6
    new_trials[0].save()

    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, [], 1)
    new_trials[0].status = "Completed"
    new_trials[0].objective_value = 0.7
    new_trials[0].save()

    new_trials = tpeAlgorithm.get_new_suggestions(self.study.id, [], 3)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 3)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertTrue(
        0.99 >= new_parameter_values_json["l1_normalization"] >= 0.01)
    self.assertTrue(0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)
    self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
    self.assertTrue(new_parameter_values_json["optimizer"] in [
        "sgd", "adagrad", "adam", "ftrl"
    ])
