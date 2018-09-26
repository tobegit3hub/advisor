from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class QuasiRandomSearchAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with quasi random search algorithm.
  """

  def __init__(self):
    super(QuasiRandomSearchAlgorithm, self).__init__("QuasiRandom")
