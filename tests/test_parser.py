import unittest

from ..parser import func


class TestMe(unittest.TestCase):

    def test_me(self):

        self.assertEqual(func(), 1)
