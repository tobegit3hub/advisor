import unittest

from .local_runner import LocalRunner


class TestLocalRunner(unittest.TestCase):
  def test(self):
    self.assertEqual(1, 1)

  def test2(self):
    runner = LocalRunner()
    self.assertEqual(2, 2)
