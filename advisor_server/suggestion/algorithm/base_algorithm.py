from suggestion.models import Study
from suggestion.models import Trial


class BaseSuggestionAlgorithm(object):
  def get_new_suggestions(self, study_id, trials, number=1):
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
    
    Args:
      study_id: The study id.
      trials: The all trials of this study.
      number: The number of trial to return. 
    Returns:
      The array of trial objects.
    """
    return None


class BaseEarlyStopAlgorithm(object):
  def get_early_stop_trials(self, trials):
    return None
