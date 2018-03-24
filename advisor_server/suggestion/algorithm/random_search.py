import json
import random

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.base_algorithm import BaseSuggestionAlgorithm


class RandomSearchAlgorithm(BaseSuggestionAlgorithm):
  def get_random_value(self, min_value, max_value):
    return random.uniform(min_value, max_value)

  def find_closest_value_in_list(self, the_list, objective_value):
    """
    Return the closet value for the objective value in the list.
    
    :param the_list: Example: [-1.5, 1.5, 2.5, 4.5]
    :param objective_value: Example: 1.1
    :return: Example: 1.5
    """
    closest_value = the_list[0]
    for current_value in the_list:
      if abs(current_value - objective_value) < abs(closest_value -
                                                    objective_value):
        closest_value = current_value
    return closest_value

  def get_new_suggestions(self, study_id, trials, number=1):
    """
    Get the new suggested trials with random search.
    """
    study = Study.objects.get(id=study_id)

    result = []
    for i in range(number):
      trial = Trial.create(study.id, "RandomSearchTrial")
      parameter_values_json = {}

      study_configuration_json = json.loads(study.study_configuration)
      params = study_configuration_json["params"]

      for param in params:

        if param["type"] == "DOUBLE":
          min_value = param["minValue"]
          max_value = param["maxValue"]
          selected_value = self.get_random_value(min_value, max_value)
          parameter_values_json[param["parameterName"]] = selected_value
        elif param["type"] == "INTEGER":
          min_value = param["minValue"]
          max_value = param["maxValue"]
          random_value = self.get_random_value(min_value, max_value)
          selected_value = int(round(random_value))
          parameter_values_json[param["parameterName"]] = selected_value
        elif param["type"] == "DISCRETE":
          feasible_points_string = param["feasiblePoints"]
          feasible_points = [
              float(value.strip())
              for value in feasible_points_string.split(",")
          ]
          feasible_points.sort()
          min_value = feasible_points[0]
          max_value = feasible_points[-1]
          random_value = self.get_random_value(min_value, max_value)
          selected_value = self.find_closest_value_in_list(
              feasible_points, random_value)
          parameter_values_json[param["parameterName"]] = selected_value
        elif param["type"] == "CATEGORICAL":
          feasible_points_string = param["feasiblePoints"]
          feasible_points = [
              value.strip() for value in feasible_points_string.split(",")
          ]
          random_value = random.randint(0, len(feasible_points) - 1)
          selected_value = feasible_points[random_value]
          parameter_values_json[param["parameterName"]] = selected_value

      trial.parameter_values = json.dumps(parameter_values_json)
      trial.save()
      result.append(trial)

    return result
