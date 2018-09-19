from suggestion.algorithm.base_hyperopt_algorithm import BaseHyperoptAlgorithm


class HyperoptRandomSearchAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with random search algorithm.
  """

  def __init__(self):
    super(HyperoptRandomSearchAlgorithm, self).__init__("random_search")
