import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.bayesian_optimization import BayesianOptimizationDemo
from suggestion.algorithm.bayesian_optimization import BayesianOptimization


class BayesianOptimizationDemoTest(TestCase):
  def test_bayes_optimizaion(self):
    algorithm = BayesianOptimizationDemo()
    algorithm.test_bayes_optimizaion()


class BayesianOptimizationTest(TestCase):
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
    self.study = Study.create("BayesianOptimizationStudy", study_configuration)
    self.trials = []

  def tearDown(self):
    pass

  def test_init(self):
    bayesianOptimization = BayesianOptimization()
    self.assertEqual(bayesianOptimization.__class__, BayesianOptimization)

  def test_get_new_suggestions(self):
    bayesianOptimization = BayesianOptimization()

    new_trials = bayesianOptimization.get_new_suggestions(self.study.id, [], 1)
    new_trials[0].status = "Completed"
    new_trials[0].objective_value = 0.6
    new_trials[0].save()

    new_trials = bayesianOptimization.get_new_suggestions(self.study.id, [], 1)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 1)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertTrue(10 >= new_parameter_values_json["hidden1"] >= 1)
    self.assertTrue(0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)
    self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
    self.assertTrue(new_parameter_values_json["optimizer"] in [
        "sgd", "adagrad", "adam", "ftrl"
    ])
    self.assertTrue(
        new_parameter_values_json["batch_normalization"] in ["true", "false"])
