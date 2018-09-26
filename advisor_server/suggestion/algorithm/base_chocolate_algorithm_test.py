from django.test import TestCase

from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.base_chocolate_algorithm import BaseChocolateAlgorithm


class BaseChocolateAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_init(self):
    instance = BaseChocolateAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, BaseChocolateAlgorithm)
