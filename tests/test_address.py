import unittest

from cardano.address import Address
from cardano.consts import Era


class TestAddress(unittest.TestCase):
    def test_valid_shelley(self):
        ADDR = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4"
        addr = Address(ADDR)
        self.assertEqual(addr.era, Era.SHELLEY)

    def test_invalid_shelley(self):     # this is known to FAIL
        ADDR = "addr1v8fet8gavr6elqt6q50XXXXf025zthqu6vr56l5k39sp9aqlvz2g4"
        with self.assertRaises(ValueError):
            Address(ADDR)


class TestComparisons(unittest.TestCase):
    def test_cmp_same_address(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)

    def test_cmp_address_to_string(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4"
        self.assertEqual(addr1, addr2)

    def test_cmp_string_to_address(self):
        addr1 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4"
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)
