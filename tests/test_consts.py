import unittest

from cardano.consts import Era


class EraTestCase(unittest.TestCase):
    def test_ltgt(self):
        self.assertTrue(
            Era.BYRON < Era.SHELLEY < Era.ALLEGRA < Era.MARY < Era.GOGUEN < Era.BASHO < Era.VOLTAIRE
        )
        self.assertTrue(
            Era.VOLTAIRE > Era.BASHO > Era.GOGUEN > Era.MARY > Era.ALLEGRA > Era.SHELLEY > Era.BYRON
        )
