from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class ChocolateRandomSearchAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with random search algorithm.
  """

  def __init__(self):
    super(ChocolateRandomSearchAlgorithm, self).__init__("Random")
