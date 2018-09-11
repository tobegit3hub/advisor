import abc


class AbstractEarlyStopAlgorithm(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_early_stop_trials(self, trials):
    """
    Pass the trials and return the list of trials to early stop.
    
    Args:
      trials: The all trials of this study.
    Returns:
      The array of trial objects.
    """
    raise NotImplementedError
