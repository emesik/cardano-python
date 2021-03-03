from decimal import Decimal
import unittest

from cardano.numbers import to_lovelaces, from_lovelaces, as_ada

class NumbersTestCase(unittest.TestCase):
    def test_simple_numbers(self):
        self.assertEqual(to_lovelaces(Decimal('0')), 0)
        self.assertEqual(from_lovelaces(0), Decimal('0'))
        self.assertEqual(to_lovelaces(Decimal('1')), 1000000)
        self.assertEqual(from_lovelaces(1000000), Decimal('1'))
        self.assertEqual(to_lovelaces(Decimal('0.000001')), 1)
        self.assertEqual(from_lovelaces(1), Decimal('0.000001'))

    def test_numeric_types(self):
        self.assertTrue(to_lovelaces(1))
        with self.assertWarns(RuntimeWarning):
            self.assertTrue(to_lovelaces(1.0))
        self.assertRaises(ValueError, to_lovelaces, '1')

    def test_rounding(self):
        self.assertEqual(to_lovelaces(Decimal('1.0000004')), 1000000)
        self.assertEqual(as_ada(Decimal('1.0000014')), Decimal('1.000001'))
