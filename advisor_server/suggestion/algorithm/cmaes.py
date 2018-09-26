from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class CmaesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with CMAES algorithm.
  """

  def __init__(self):
    super(CmaesAlgorithm, self).__init__("CMAES")
