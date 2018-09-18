from suggestion.algorithm.base_hyperopt_algorithm import BaseHyperoptAlgorithm


class SimulateAnnealAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with simulate anneal algorithm.
  """

  def __init__(self):
    super(SimulateAnnealAlgorithm, self).__init__("anneal")
