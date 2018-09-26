#!/usr/bin/env python

import json

from advisor_client.model import Study
from advisor_client.model import Trial
from advisor_client.model import TrialMetric
from advisor_client.client import AdvisorClient

client = AdvisorClient()

# Create Study
name = "Study"
maxTrials = 20
study_configuration = {
    #"goal":
    # "MAXIMIZE",
    "goal":
    "MINIMIZE",
    "maxTrials":
    maxTrials,
    "maxParallelTrials":
    1,
    "randomInitTrials":
    10,
    "params": [{
        "parameterName": "x",
        "type": "DOUBLE",
        "minValue": -10,
        "maxValue": 10,
        "scallingType": "LINEAR"
    }]
}

#algorithm = "RandomSearch"
algorithm = "BayesianOptimization"
#algorithm = "TPE"
#algorithm = "SimulateAnneal"
#algorithm = "QuasiRandomSearch"
#algorithm = "ChocolateRandomSearch"
#algorithm = "ChocolateBayes"
#algorithm = "CMAES"
#algorithm = "MOCMAES"

study = client.create_study(name, study_configuration, algorithm=algorithm)
print(study)

for i in range(maxTrials):
  trial = client.get_suggestions(study.id, 1)[0]
  parameter_value_dict = json.loads(trial.parameter_values)
  x = parameter_value_dict['x']
  #metric = -(x * x - 3 * x + 2)
  metric = x * x - 3 * x + 2
  trial = client.complete_trial_with_one_metric(trial, metric)
  print(trial)

best_trial = client.get_best_trial(study.id)
print("Best trial: {}".format(best_trial))
