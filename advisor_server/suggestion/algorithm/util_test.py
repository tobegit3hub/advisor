from django.test import TestCase

from suggestion.algorithm.util import AlgorithmUtil


class AlgorithmUtilTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_get_random_value(self):
    min_value = 1.0
    max_value = 10.0
    value = AlgorithmUtil.get_random_value(min_value, max_value)
    self.assertTrue(value >= min_value)
    self.assertTrue(value <= max_value)

    min_value = -10.0
    max_value = -1.0
    value = AlgorithmUtil.get_random_value(min_value, max_value)
    self.assertTrue(value >= min_value)
    self.assertTrue(value <= max_value)

  def test_get_random_int_value(self):
    min_value = 1
    max_value = 10
    value = AlgorithmUtil.get_random_int_value(min_value, max_value)
    self.assertTrue(value >= min_value)
    self.assertTrue(value <= max_value)
    self.assertTrue(isinstance(value, int))

    min_value = -10
    max_value = -1
    value = AlgorithmUtil.get_random_int_value(min_value, max_value)
    self.assertTrue(value >= min_value)
    self.assertTrue(value <= max_value)
    self.assertTrue(isinstance(value, int))

  def test_get_closest_value_in_list(self):
    input_list = [-1.5, 1.5, 2.5, 4.5]
    objective_value = 1.1
    value = AlgorithmUtil.get_closest_value_in_list(input_list,
                                                    objective_value)
    self.assertEqual(value, 1.5)

    input_list = [-1.5, 1.5, 2.5, 4.5]
    objective_value = 5.0
    value = AlgorithmUtil.get_closest_value_in_list(input_list,
                                                    objective_value)
    self.assertEqual(value, 4.5)

  def test_get_closest_value_in_list(self):
    input_list = [1.5, -1.5, 2.5, 4.5]
    value = AlgorithmUtil.get_random_item_from_list(input_list)
    self.assertTrue(value in input_list)
