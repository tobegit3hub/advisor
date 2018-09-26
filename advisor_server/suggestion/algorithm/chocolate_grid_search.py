from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class ChocolateGridSearchAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with grid search algorithm.
  """

  def __init__(self):
    super(ChocolateGridSearchAlgorithm, self).__init__("Grid")
