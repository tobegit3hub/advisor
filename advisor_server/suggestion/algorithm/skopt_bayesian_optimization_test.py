import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.skopt_bayesian_optimization import SkoptBayesianOptimization


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
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("SkoptBayesianOptimizationStudy", study_configuration)

  def tearDown(self):
    pass

  def test_init(self):
    instance = SkoptBayesianOptimization()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, SkoptBayesianOptimization)

  def test_get_new_suggestions(self):
    algorithm = SkoptBayesianOptimization()

    new_trials = algorithm.get_new_suggestions(
        self.study.id, number=1)
    new_trial = new_trials[0]
    new_parameter_values_json = json.loads(new_trial.parameter_values)

    self.assertTrue(10 >= new_parameter_values_json["hidden1"] >= 1)
    self.assertTrue(0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)

  def test_get_multiple_new_suggestions(self):
    algorithm = SkoptBayesianOptimization()

    # Assert getting one trial
    new_trials = algorithm.get_new_suggestions(
        self.study.id, number=1)
    self.assertEqual(len(new_trials), 1)

    # Assert getting multiple trials
    new_trials = algorithm.get_new_suggestions(
        self.study.id, number=10)
    self.assertEqual(len(new_trials), 10)
