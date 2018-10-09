import json
import yaml
import logging
import subprocess
import coloredlogs

from .abstract_runner import AbstractRunner
from .local_runner import LocalRunner

from advisor_client.client import AdvisorClient

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("simple_tensorflow_serving")
logger.setLevel(logging.DEBUG)

coloredlogs.install(
    level='DEBUG', logger=logger, fmt='%(asctime)s %(levelname)s %(message)s')


class RunnerLauncher():
  def __init__(self, run_file=None):

    # Example: {u'name': u'simple1', u'algorithm': u'RandomSearch', u'runner': u'local_runner', u'search_space': {u'maxTrials': 5, u'params': [{u'scalingType': u'LINEAR', u'type': u'DOUBLE', u'maxValue': 0.01, u'minValue': 0.001, u'parameterName': u'gamma', u'feasiblePoints': u''}], u'randomInitTrials': 1, u'goal': u'MINIMIZE', u'maxParallelTrials': 1}, u'trialNumber':3, u'concurrency': 1, u'path': u'~/code/', u'command': u'python ./simple_function.py'}
    self.run_config_dict = {}

    with open(run_file, "r") as f:

      if run_file.endswith(".json"):
        self.run_config_dict = json.load(f)
      elif run_file.endswith(".yml") or run_file.endswith(".yaml"):
        self.run_config_dict = yaml.safe_load(f)
      else:
        logging.error("Unsupport config file format, use json or yaml")

      logging.info("Run with config: {}".format(self.run_config_dict))

  def run(self):
    client = AdvisorClient()

    self.run_config_dict

    # TODO: move the logic into local runner
    runner = LocalRunner()
    if "runner" in self.run_config_dict:
      if self.run_config_dict["runner"] == "local_runner":
        runner = LocalRunner()
        logging.info("Run with local runner")

    study_name = self.run_config_dict["name"].encode("utf-8")
    study = client.get_or_create_study(study_name,
                                       self.run_config_dict["search_space"],
                                       self.run_config_dict["algorithm"])

    logging.info("Create study: {}".format(study))

    for i in range(self.run_config_dict["trialNumber"]):

      logging.info("-------------------- Start Trial --------------------")

      # Get suggested trials
      trials = client.get_suggestions(study.name, 1)

      logging.info("Get trial: {}".format(trials[0]))

      #import ipdb;ipdb.set_trace()

      # Generate parameters
      parameter_value_dicts = []
      for trial in trials:
        parameter_value_dict = json.loads(trial.parameter_values)
        logging.info(
            "The suggested parameters: {}".format(parameter_value_dict))
        parameter_value_dicts.append(parameter_value_dict)

      # Run training

      for trial in trials:
        #metric = train_function(**parameter_value_dicts[i])

        # Example: {"gamma": 0.0063987614450157415}
        parameters_dict = json.loads(trials[0].parameter_values)
        parameter_string = ""

        for k, v in parameters_dict.items():
          parameter_string += " -{}={}".format(k, v)

        command_string = "cd {} && {} {}".format(
            self.run_config_dict["path"], self.run_config_dict["command"],
            parameter_string)

        #exit_code = subprocess.call(command_string, shell=True)
        logging.info("Run the command: {}".format(command_string))

        # Example: '0.0\n'
        # Example: 'Compute y = x * x - 3 * x + 2\nIput x is: 1.0\nOutput is: 0.0\n0.0\n'
        command_output = subprocess.check_output(command_string, shell=True)
        # TODO: Log the output in the directory
        #logging.info("Get output of command: {}".format(command_output))

        metric = float(command_output.split("\n")[-2].strip())
        # Complete the trial
        client.complete_trial_with_one_metric(trial, metric)
        logging.info("Update the trial with metrics: {}".format(metric))

      logging.info("--------------------- End Trial ---------------------")

    is_done = client.is_study_done(study.name)
    best_trial = client.get_best_trial(study.name)
    logging.info("The study: {}, best trial: {}".format(study, best_trial))
