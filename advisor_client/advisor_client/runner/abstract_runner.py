import abc


class AbstractRunner(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def run(self, study_name, trials=[], number=1):
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
                      "scalingType": "LINEAR"
                  }
              ]
          }
        
        The trial's parameter_values_json should be like this.
        {
              "hidden1": 40
        }
        
        Args:
          study_name: The study name.
          trials: The all trials of this study.
          number: The number of trial to return. 
        Returns:
          The array of trial objects.
        """
    raise NotImplementedError
