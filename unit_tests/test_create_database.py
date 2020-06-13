from create_database import *
import unittest

class MyFirstTest(unittest.TestCase):
    def test_case_01(self):
        self.assertEqual(1, 1)