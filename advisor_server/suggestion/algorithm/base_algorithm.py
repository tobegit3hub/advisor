from suggestion.models import Study
from suggestion.models import Trial


class BaseSuggestionAlgorithm(object):
  """
  The study's study_configuration is like this.
  {
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
  
  The trial's parameter_values_json should be like this.
  {
        "hidden1": 40
  }
  """
  def get_new_suggestions(self, trials, number=1):
    pass


class BaseEarlyStopAlgorithm(object):
  def get_early_stop_trials(self, trials):
    pass


class NoEarlyStopAlgorithm(object):
  def get_early_stop_trials(self, trials):
    return trials