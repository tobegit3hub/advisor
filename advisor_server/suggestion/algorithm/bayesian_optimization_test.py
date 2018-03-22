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
    bayesianOptimization = BayesianOptimization()
    self.assertEqual(bayesianOptimization.__class__, BayesianOptimization)

  def test_get_new_suggestions(self):
    bayesianOptimization = BayesianOptimization()

    new_trials = bayesianOptimization.get_new_suggestions(
        self.study.id, self.trials, 1)
    new_trials[0].status = "Completed"
    new_trials[0].parameter_values = '{"hidden1": 50}'
    new_trials[0].objective_value = 0.6
    new_trials[0].save()
    new_trials = bayesianOptimization.get_new_suggestions(
        self.study.id, self.trials, 1)
    new_trials[0].status = "Completed"
    new_trials[0].parameter_values = '{"hidden1": 150}'
    new_trials[0].objective_value = 0.8
    new_trials[0].save()
    new_trials = bayesianOptimization.get_new_suggestions(
        self.study.id, self.trials, 1)
    new_trials[0].status = "Completed"
    new_trials[0].parameter_values = '{"hidden1": 250}'
    new_trials[0].objective_value = 0.6
    new_trials[0].save()
    new_trials = bayesianOptimization.get_new_suggestions(
        self.study.id, self.trials, 1)

    # Assert getting two trials
    self.assertEqual(len(new_trials), 1)

    # Assert getting the trials
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    #self.assertEqual(new_parameter_values_json["hidden1"], 40)
