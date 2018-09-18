from suggestion.algorithm.base_hyperopt_algorithm import BaseHyperoptAlgorithm


class TpeAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with TPE algorithm.
  """

  def __init__(self):
    super(TpeAlgorithm, self).__init__("tpe")
