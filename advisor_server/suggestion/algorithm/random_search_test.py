import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from random_search import RandomSearchAlgorithm


class RandomSearchAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_init(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()
    self.assertEqual(randomSearchAlgorithm.__class__, RandomSearchAlgorithm)

  def test_get_new_suggestions(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()

    study_configuration_json = {
      "goal": "MAXIMIZE",
      "maxTrials": 5,
      "maxParallelTrials": 1,
      "params": [
        {
          "parameterName": "hidden1",
          "type": "INTEGER",
          "minValue": 40,
          "maxValue": 400,
          "scallingType": "LINEAR"
        }
      ]
    }
    study_configuration = json.dumps(study_configuration_json)
    study = Study.create("RandomSearchStudy", study_configuration)
    trial = Trial.create(study.id, "RandomSearchTrial")
    trials = [trial]
    new_trials = randomSearchAlgorithm.get_new_suggestions(trials)

    # Assert get one trial
    self.assertEqual(len(new_trials), 1)

    # Assert get the random trial
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertTrue("hidden1" in new_parameter_values_json)
    self.assertTrue(new_parameter_values_json["hidden1"] >= 40)
    self.assertTrue(new_parameter_values_json["hidden1"] <= 400)

