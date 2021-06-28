import unittest

from cardano.address import (
    address,
    Address,
    ByronAddress,
    IcarusAddress,
    ShelleyAddress,
)
from cardano.consts import Era

from .example_addresses import (
    GENERAL_ERR,
    ICARUS_OK,
    BYRON_OK,
    SHELLEY_OK,
    ICARUS_ERR,
    BYRON_ERR,
    SHELLEY_ERR,
)


class BaseTestAddressOK(object):
    address_list = None
    AddressClass = None

    def test_address(self):
        for addr in self.address_list:
            addrobj = address(addr)
            self.assertIsInstance(addrobj, self.AddressClass)


class TestByronAddressOK(BaseTestAddressOK, unittest.TestCase):
    address_list = BYRON_OK
    AddressClass = ByronAddress


class TestIcarusAddressOK(BaseTestAddressOK, unittest.TestCase):
    address_list = ICARUS_OK
    AddressClass = IcarusAddress


class TestShelleyAddressOK(BaseTestAddressOK, unittest.TestCase):
    address_list = SHELLEY_OK
    AddressClass = ShelleyAddress


class TestAddressERR(unittest.TestCase):
    def test_address(self):
        for addr in GENERAL_ERR + BYRON_ERR + ICARUS_ERR + SHELLEY_ERR:
            self.assertRaises(ValueError, address, addr)


class TestComparisons(unittest.TestCase):
    def test_cmp_same_address(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)

    def test_cmp_different_address(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = Address(
            "addr1XXX"
        )  # TODO: put some real address here once validation present
        self.assertNotEqual(addr1, addr2)

    def test_cmp_address_to_string(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4"
        self.assertEqual(addr1, addr2)

    def test_cmp_string_to_address(self):
        addr1 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4"
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)

    def test_cmp_address_to_bytes(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4".encode()
        self.assertEqual(addr1, addr2)

    def test_cmp_bytes_to_address(self):
        addr1 = "addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4".encode()
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)

    def test_cmp_address_to_none(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertNotEqual(addr1, None)
