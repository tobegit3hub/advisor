import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from random_search import RandomSearchAlgorithm
from particle_swarm_optimization import ParticleSwarmOptimization


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
            "scalingType": "LtINEAR"
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("RandomSearchStudy", study_configuration)
    trial = Trial.create(self.study.id, "RandomSearchTrial")
    self.trials = [trial]

  def tearDown(self):
    pass

  def test_init(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()
    self.assertEqual(randomSearchAlgorithm.__class__, RandomSearchAlgorithm)

  def test_get_new_suggestions(self):
    randomSearchAlgorithm = RandomSearchAlgorithm()
    new_trials = randomSearchAlgorithm.get_new_suggestions(
        self.study.id, self.trials)

    # Assert getting one trial
    self.assertEqual(len(new_trials), 1)

    # Assert getting the random trial
    new_trial = new_trials[0]
    new_parameter_values = new_trial.parameter_values
    new_parameter_values_json = json.loads(new_parameter_values)
    self.assertTrue("hidden1" in new_parameter_values_json)
    self.assertTrue(new_parameter_values_json["hidden1"] >= 40)
    self.assertTrue(new_parameter_values_json["hidden1"] <= 400)

  def test_hello(self):
    particleSwarmOptimization = ParticleSwarmOptimization()
    particleSwarmOptimization.run_pso_demo()
