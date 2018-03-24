import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.base_algorithm import BaseSuggestionAlgorithm
from suggestion.algorithm.base_algorithm import BaseEarlyStopAlgorithm


class RandomSearchAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_init(self):
    baseSuggestionAlgorithm = BaseSuggestionAlgorithm()
    self.assertEqual(baseSuggestionAlgorithm.__class__,
                     BaseSuggestionAlgorithm)

    baseEarlyStopAlgorithm = BaseEarlyStopAlgorithm()
    self.assertEqual(baseEarlyStopAlgorithm.__class__, BaseEarlyStopAlgorithm)
