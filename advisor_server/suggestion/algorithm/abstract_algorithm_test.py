from django.test import TestCase

from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm


class TestAbstractSuggestionAlgorithm(AbstractSuggestionAlgorithm):
  """
  Construct the test class to implement AbstractSuggestionAlgorithm.
  """

  def get_new_suggestions(self, study_name, trials=[], number=1):
    return []


class RandomSearchAlgorithmTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_subclass(self):

    instance = TestAbstractSuggestionAlgorithm()

    # Test if it is AbstractSuggestionAlgorithm
    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    # Test if it is TestAbstractSuggestionAlgorithm
    self.assertTrue(isinstance(instance, TestAbstractSuggestionAlgorithm))
    self.assertEqual(instance.__class__, TestAbstractSuggestionAlgorithm)

  def test_get_new_suggestions(self):

    instance = TestAbstractSuggestionAlgorithm()

    # Test get_new_suggestions function
    study_name = "test"
    self.assertEqual(len(instance.get_new_suggestions(study_name)), 0)
