import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.models import TrialMetric
from suggestion.algorithm.early_stop_algorithm import NoEarlyStopAlgorithm
from suggestion.algorithm.early_stop_algorithm import EarlyStopFirstTrialAlgorithm
from suggestion.algorithm.early_stop_algorithm import EarlyStopDescendingAlgorithm


class RandomSearchAlgorithmTest(TestCase):
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
    self.study = Study.create("RandomSearchStudy", study_configuration)
    trial1 = Trial.create(self.study.id, "RandomSearchTrial1")
    trial2 = Trial.create(self.study.id, "RandomSearchTrial2")
    self.trials = [trial1, trial2]
    TrialMetric.create(trial1.id, 10, 0.5)
    TrialMetric.create(trial1.id, 20, 0.6)
    TrialMetric.create(trial2.id, 10, 0.6)
    TrialMetric.create(trial2.id, 20, 0.5)

  def tearDown(self):
    pass

  def test_init(self):
    algorithm = NoEarlyStopAlgorithm()
    self.assertEqual(algorithm.__class__, NoEarlyStopAlgorithm)

  # Test NoEarlyStopAlgorithm
  def test_get_early_stop_trials1(self):
    algorithm = NoEarlyStopAlgorithm()
    early_stop_trials = algorithm.get_early_stop_trials(self.trials)
    self.assertEqual(len(early_stop_trials), 0)

  # Test EarlyStopFirstTrialAlgorithm
  def test_get_early_stop_trials1(self):
    algorithm = EarlyStopFirstTrialAlgorithm()
    early_stop_trials = algorithm.get_early_stop_trials(self.trials)
    self.assertEqual(len(early_stop_trials), 1)
    self.assertEqual(early_stop_trials[0].name, "RandomSearchTrial1")

  # Test EarlyStopDescendingAlgorithm
  def test_get_early_stop_trials1(self):
    algorithm = EarlyStopDescendingAlgorithm()
    early_stop_trials = algorithm.get_early_stop_trials(self.trials)
    self.assertEqual(len(early_stop_trials), 1)
    self.assertEqual(early_stop_trials[0].name, "RandomSearchTrial2")
