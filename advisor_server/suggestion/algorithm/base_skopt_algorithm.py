import json
import numpy as np
import skopt

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm


class BaseSkoptAlgorithm(AbstractSuggestionAlgorithm):
  """
  Refer to https://github.com/scikit-optimize/scikit-optimize .
  """

  def __init__(self, algorithm_name="bayesian_optimization"):

    self.algorithm_name = algorithm_name


  def get_new_suggestions(self, study_name, input_trials=[], number=1):
    """
    Get the new suggested trials with skopt algorithm.
    """

    # Construct search space, example: {"x": hyperopt.hp.uniform('x', -10, 10), "x2": hyperopt.hp.uniform('x2', -10, 10)}
    hyperopt_search_space = {}

    study = Study.objects.get(name=study_name)
    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    skopt_search_space  = []


    for param in params:
      param_name = param["parameterName"]

      if param["type"] == "INTEGER":
        skopt_search_space.append(skopt.space.Integer(param["minValue"], param["maxValue"], name='min_samples_leaf'))

      elif param["type"] == "DOUBLE":
        skopt_search_space.append(skopt.space.Real(param["minValue"], param["maxValue"], "log-uniform", name='learning_rate'))

      elif param["type"] == "DISCRETE" or param["type"] == "CATEGORICAL":
        pass


    if self.algorithm_name == "bayesian_optimization":
      skopt_optimizer = skopt.Optimizer([(-2.0, 2.0)])
    else:
      print("Unsupport skopt algorithm: {}".format(self.algorithm_name))


    completed_advisor_trials = Trial.objects.filter(
        study_name=study_name, status="Completed")

    for index, advisor_trial in enumerate(completed_advisor_trials):
      # Example: {"learning_rate": 0.01, "optimizer": "ftrl"}
      parameter_values_json = json.loads(advisor_trial.parameter_values)


      # Example: [(-2.0, 2.0)]
      skopt_suggested = []

      for param in params:

        if param["type"] == "INTEGER" or param["type"] == "DOUBLE":
          parameter_value = parameter_values_json[param["parameterName"]]
          skopt_suggested.append(parameter_value)

        elif param["type"] == "DISCRETE":
          pass

        elif param["type"] == "CATEGORICAL":
          pass

      loss_for_skopt = advisor_trial.objective_value
      if study_configuration_json["goal"] == "MAXIMIZE":
        # Now hyperopt only supports fmin and we need to reverse objective value for maximization
        loss_for_skopt = -1 * advisor_trial.objective_value

      skopt_optimizer.tell(skopt_suggested, loss_for_skopt)


    return_trial_list = []

    for i in range(number):

      skopt_suggested = skopt_optimizer.ask()

      new_advisor_trial = Trial.create(study.name, "SkoptTrial")
      parameter_values_json = {}

      index = 0
      for param in params:

        if param["type"] == "INTEGER" or param["type"] == "DOUBLE":
          parameter_values_json[param["parameterName"]] = skopt_suggested[index]

        elif param["type"] == "DISCRETE":
          pass

        elif param["type"] == "CATEGORICAL":
          pass

        index += 1

      new_advisor_trial.parameter_values = json.dumps(parameter_values_json)
      new_advisor_trial.save()
      return_trial_list.append(new_advisor_trial)

    return return_trial_list
