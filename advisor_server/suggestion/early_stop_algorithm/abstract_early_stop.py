import abc


class AbstractEarlyStopAlgorithm(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_early_stop_trials(self, trials):
    raise NotImplementedError
