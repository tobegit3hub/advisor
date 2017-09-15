import json
import random

from suggestion.models import Study
from suggestion.models import Trial
from base_algorithm import BaseSuggestionAlgorithm


class RandomSearchAlgorithm(BaseSuggestionAlgorithm):
  def get_random_value(self, min_value, max_value):
    return random.uniform(min_value, max_value)

  def get_new_suggestions(self, trials, number=1):
    """
    Get the new suggested trials with random search.
    """
    old_trial = trials[0]
    study = Study.objects.get(id=old_trial.study_id)

    result = []
    for i in range(number):
      trial = Trial.create(study.id, "RandomSearchTrial")
      parameter_values_json = {}

      study_configuration_json = json.loads(study.study_configuration)
      params = study_configuration_json["params"]
      for param in params:
        min_value = param["minValue"]
        max_value = param["maxValue"]
        random_value = self.get_random_value(min_value, max_value)
        parameter_values_json[param["parameterName"]] = random_value

      trial.parameter_values = json.dumps(parameter_values_json)
      result.append(trial)

    return result
