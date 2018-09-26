from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class MocmaesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with MOCMAES algorithm.
  """

  def __init__(self):
    super(MocmaesAlgorithm, self).__init__("MOCMAES")
