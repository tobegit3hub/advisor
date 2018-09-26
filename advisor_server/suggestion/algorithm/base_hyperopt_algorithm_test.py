from django.test import TestCase

from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.base_hyperopt_algorithm import BaseHyperoptAlgorithm


class BaseHyperoptAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_init(self):
    instance = BaseHyperoptAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, BaseHyperoptAlgorithm)
