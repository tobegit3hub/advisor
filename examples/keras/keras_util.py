#!/usr/bin/env python

import json

from advisor_client.client import AdvisorClient


def main(train_function):
  client = AdvisorClient()

  # Get or create the study
  study_configuration = {
      "goal":
      "MINIMIZE",
      "randomInitTrials":
      1,
      "maxTrials":
      5,
      "maxParallelTrials":
      1,
      "params": [
          {
              "parameterName": "filter_number0",
              "type": "INTEGER",
              "minValue": 16,
              "maxValue": 32,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
          {
              "parameterName": "convolution_kernel_size0",
              "type": "INTEGER",
              "minValue": 3,
              "maxValue": 5,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
          {
              "parameterName": "max_polling_size0",
              "type": "INTEGER",
              "minValue": 2,
              "maxValue": 3,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
          {
              "parameterName": "filter_number1",
              "type": "INTEGER",
              "minValue": 16,
              "maxValue": 32,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
          {
              "parameterName": "convolution_kernel_size1",
              "type": "INTEGER",
              "minValue": 3,
              "maxValue": 5,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
          {
              "parameterName": "max_polling_size1",
              "type": "INTEGER",
              "minValue": 2,
              "maxValue": 3,
              "feasiblePoints": "",
              "scallingType": "LINEAR"
          },
      ]
  }
  #study = client.create_study("Study", study_configuration, "BayesianOptimization")
  study = client.create_study("Study", study_configuration,
                              "RandomSearchAlgorithm")
  #study = client.get_study_by_id(6)

  # Get suggested trials
  trials = client.get_suggestions(study.id, 3)

  #import ipdb;ipdb.set_trace()

  # Generate parameters
  parameter_value_dicts = []
  for trial in trials:
    parameter_value_dict = json.loads(trial.parameter_values)
    print("The suggested parameters: {}".format(parameter_value_dict))
    parameter_value_dicts.append(parameter_value_dict)

  # Run training
  metrics = []
  for i in range(len(trials)):
    metric = train_function(**parameter_value_dicts[i])
    #metric = train_function(parameter_value_dicts[i])
    metrics.append(metric)

    trial = trials[i]
    # Complete the trial
    client.complete_trial_with_one_metric(trial, metrics[i])

  is_done = client.is_study_done(study.id)
  best_trial = client.get_best_trial(study.id)
  print("The study: {}, best trial: {}".format(study, best_trial))


if __name__ == "__main__":
  main()
