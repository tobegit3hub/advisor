from django.test import TestCase

from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.base_skopt_algorithm import BaseSkoptAlgorithm


class BaseSkoptAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_init(self):
    instance = BaseSkoptAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, BaseSkoptAlgorithm)
