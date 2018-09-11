from suggestion.early_stop_algorithm.abstract_early_stop import AbstractEarlyStopAlgorithm


class NoEarlyStopAlgorithm(AbstractEarlyStopAlgorithm):
  def get_early_stop_trials(self, trials):
    return []
