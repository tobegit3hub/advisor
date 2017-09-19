#!/usr/bin/env python

import json
import subprocess
import tensorflow as tf

from advisor_client.model import Study
from advisor_client.model import Trial
from advisor_client.model import TrialMetric
from advisor_client.client import AdvisorClient
import tensorboard_util


def main():
  client = AdvisorClient()

  # Create the study
  name = "Study"
  study_configuration = {
      "goal":
      "MINIMIZE",
      "maxTrials":
      5,
      "maxParallelTrials":
      1,
      "params": [{
          "parameterName": "learning_rate",
          "type": "INTEGER",
          "minValue": 0.01,
          "maxValue": 0.1,
          "scallingType": "LINEAR"
      }]
  }
  study = client.create_study(name, study_configuration)

  # Get suggested trials
  trials = client.get_suggestions(study.id, 3)

  # Generate command-line parameters
  commandline_parameters = []
  i = 0
  for trial in trials:
    parameter = "--output_path=output/{}".format(i)
    parameter_value_dict = json.loads(trial.parameter_values)

    # Example: {"learning_rate": 0.05943265431983244}
    for k, v in parameter_value_dict.items():
      parameter += " --{}={}".format(k, v)

    print(parameter)
    commandline_parameters.append(parameter)
    i += 1

  # Run training
  for i in range(3):
    module_args = commandline_parameters[i]
    module_name = "trainer.task"
    # Example: python -m trainer.task --output_path=0 --learning_rate=0.0796523079087
    shell_command = "python -m {} {}".format(module_name, module_args)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

  # Complete the trial
  for i in range(3):
    trial = trials[i]
    logdir = "output/{}".format(i)
    tensorboard_metrics = tensorboard_util.get_hyperparameters_metric(logdir)
    client.complete_trial(trial, tensorboard_metrics)

  # Check if study done
  is_done = client.is_study_done(study.id)
  best_trial = client.get_best_trial(study.id)
  print("The study: {}, if it is done: {}, best trial: {}".format(
      study, is_done, best_trial))


if __name__ == "__main__":
  main()
