import json
import itertools

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm


class GridSearchAlgorithm(AbstractSuggestionAlgorithm):
  def get_new_suggestions(self, study_name, trials=[], number=1):
    """
    Get the new suggested trials with grid search.
    """

    return_trial_list = []

    study = Study.objects.get(name=study_name)

    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]
    param_number = len(params)

    # [['8', '16', '32', '64'], ['sgd', 'adagrad', 'adam', 'ftrl'], ['true', 'false']]
    param_values_list = []

    for param in params:

      # Check param type
      if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
        raise Exception("Grid search does not support DOUBLE and INTEGER")

      feasible_point_list = [
          value.strip() for value in param["feasiblePoints"].split(",")
      ]

      param_values_list.append(feasible_point_list)

    # Example: [('8', 'sgd', 'true'), ('8', 'sgd', 'false'), ('8', 'adagrad', 'true'), ('8', 'adagrad', 'false'), ('8', 'adam', 'true'), ('8', 'adam', 'false'), ('8', 'ftrl', 'true'), ('8', 'ftrl', 'false'), ('16', 'sgd', 'true'), ('16', 'sgd', 'false'), ('16', 'adagrad', 'true'), ('16', 'adagrad', 'false'), ('16', 'adam', 'true'), ('16', 'adam', 'false'), ('16', 'ftrl', 'true'), ('16', 'ftrl', 'false'), ('32', 'sgd', 'true'), ('32', 'sgd', 'false'), ('32', 'adagrad', 'true'), ('32', 'adagrad', 'false'), ('32', 'adam', 'true'), ('32', 'adam', 'false'), ('32', 'ftrl', 'true'), ('32', 'ftrl', 'false'), ('64', 'sgd', 'true'), ('64', 'sgd', 'false'), ('64', 'adagrad', 'true'), ('64', 'adagrad', 'false'), ('64', 'adam', 'true'), ('64', 'adam', 'false'), ('64', 'ftrl', 'true'), ('64', 'ftrl', 'false')]
    combination_values_list = list(itertools.product(*param_values_list))

    # Example: [{"hidden2": "8", "optimizer": "sgd", "batch_normalization": "true"}, ......]
    all_combination_values_json = []

    for combination_values in combination_values_list:

      combination_values_json = {}

      # Example: (u'8', u'sgd', u'true')
      for i in range(param_number):
        # Example: "sgd"
        combination_values_json[params[i][
            "parameterName"]] = combination_values[i]

      all_combination_values_json.append(combination_values_json)

    all_combination_number = len(all_combination_values_json)

    # Compute how many grid search params have been allocated
    allocated_trials = Trial.objects.filter(study_name=study_name)
    return_trials_start_index = len(allocated_trials)

    if return_trials_start_index > all_combination_number:
      return_trials_start_index = 0
    elif return_trials_start_index + number > all_combination_number:
      return_trials_start_index = all_combination_number - number

    for i in range(number):
      trial = Trial.create(study.name, "GridSearchTrial")
      trial.parameter_values = json.dumps(
          all_combination_values_json[return_trials_start_index + i])
      trial.save()
      return_trial_list.append(trial)

    return return_trial_list
