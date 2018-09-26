from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class ChocolateBayesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with bayes algorithm.
  """

  def __init__(self):
    super(ChocolateBayesAlgorithm, self).__init__("Bayes")
