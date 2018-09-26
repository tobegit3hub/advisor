import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.chocolate_grid_search import ChocolateGridSearchAlgorithm


class ChocolateGridSearchAlgorithmTest(TestCase):
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
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("ChocolateGridSearchStudy", study_configuration)

  def tearDown(self):
    pass

  def test_init(self):
    instance = ChocolateGridSearchAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, ChocolateGridSearchAlgorithm)

  def test_get_multiple_suggestions(self):
    instance = ChocolateGridSearchAlgorithm()

    new_trials = instance.get_new_suggestions(self.study.id, number=3)
    self.assertEqual(len(new_trials), 3)

  def test_get_new_suggestions(self):
    instance = ChocolateGridSearchAlgorithm()

    new_trials = instance.get_new_suggestions(self.study.id, number=3)
    self.assertEqual(len(new_trials), 3)

    new_trials = instance.get_new_suggestions(self.study.id, number=3)

    for new_trial in new_trials:
      new_parameter_values_json = json.loads(new_trial.parameter_values)

      self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
      self.assertTrue(new_parameter_values_json["optimizer"] in [
          "sgd", "adagrad", "adam", "ftrl"
      ])
