import unittest

from cardano.address import (
    address,
    Address,
    ByronAddress,
    IcarusAddress,
    ShelleyAddress,
)
from cardano.address.shelley import NetworkTag, AddressType, Hash, Pointer

from .example_addresses import (
    GENERAL_ERR,
    ICARUS_OK,
    BYRON_OK,
    ICARUS_ERR,
    BYRON_ERR,
    SHELLEY_ERR,
)


class BaseTestAddressOK(object):
    def test_address(self):
        for addr in self.address_list:
            addrobj = self.AddressClass(addr)
            addrobj = address(addr)
            self.assertIsInstance(addrobj, self.AddressClass)


class TestByronAddressOK(BaseTestAddressOK, unittest.TestCase):
    address_list = BYRON_OK
    AddressClass = ByronAddress


class TestIcarusAddressOK(BaseTestAddressOK, unittest.TestCase):
    address_list = ICARUS_OK
    AddressClass = IcarusAddress


class BaseTestAddressERR(object):
    address_list = set()

    def test_address(self):
        for addr in self.address_list:
            with self.assertRaises(ValueError):
                a = address(addr)
                # FIXME: hack to present verbose error messages when exception is NOT raised
                raise AssertionError(
                    '{:s} did not raise ValueError and returned "{}" of type {}'.format(
                        addr, a, type(a)
                    )
                )


class TestGeneralAddressERR(BaseTestAddressERR, unittest.TestCase):
    address_list = GENERAL_ERR


# class TestByronAddressERR(BaseTestAddressERR, unittest.TestCase):
#    address_list = BYRON_ERR


# class TestIcarusAddressERR(BaseTestAddressERR, unittest.TestCase):
#    address_list = ICARUS_ERR


class TestShelleyAddressERR(BaseTestAddressERR, unittest.TestCase):
    address_list = SHELLEY_ERR


class TestAutoRecognition(unittest.TestCase):
    def test_valid(self):
        for addr in BYRON_OK + ICARUS_OK:
            address(addr)

    def test_invalid(self):
        for addr in GENERAL_ERR + SHELLEY_ERR:  # + BYRON_ERR + ICARUS_ERR:
            self.assertRaises(ValueError, address, addr)


class TestComparisons(unittest.TestCase):
    def test_cmp_same_address(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        self.assertEqual(addr1, addr2)

    def test_cmp_different_address(self):
        addr1 = Address("addr1v8fet8gavr6elqt6q50skkjf025zthqu6vr56l5k39sp9aqlvz2g4")
        addr2 = Address("addr1XXX")
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


class TestShelleyAddressDeserialization(unittest.TestCase):
    def test_mainnet_PaymentKeyHash_StakeKeyHash(self):
        addr = ShelleyAddress(
            "addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgse35a3x"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_mainnet_ScriptHash_StakeKeyHash(self):
        addr = ShelleyAddress(
            "addr1z8phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gten0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs9yc0hh"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_mainnet_PaymentKeyHash_ScriptHash(self):
        addr = ShelleyAddress(
            "addr1yx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzerkr0vd4msrxnuwnccdxlhdjar77j6lg0wypcc9uar5d2shs2z78ve"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_mainnet_ScriptHash_ScriptHash(self):
        addr = ShelleyAddress(
            "addr1x8phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gt7r0vd4msrxnuwnccdxlhdjar77j6lg0wypcc9uar5d2shskhj42g"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_mainnet_PaymentKeyHash_Pointer(self):
        addr = ShelleyAddress(
            "addr1gx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer5pnz75xxcrzqf96k"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_Pointer)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Pointer)

    def test_mainnet_ScriptHash_Pointer(self):
        addr = ShelleyAddress(
            "addr128phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtupnz75xxcrtw79hu"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_Pointer)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Pointer)

    def test_mainnet_PaymentKeyHashOnly(self):
        addr = ShelleyAddress(
            "addr1vx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzers66hrl8"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHashOnly)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_mainnet_ScriptHashOnly(self):
        addr = ShelleyAddress(
            "addr1w8phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtcyjy7wx"
        )
        self.assertEqual(addr.hrp, "addr")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHashOnly)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_mainnet_StakeKeyHash(self):
        addr = ShelleyAddress(
            "stake1uyehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gh6ffgw"
        )
        self.assertEqual(addr.hrp, "stake")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_mainnet_ScriptHash(self):
        addr = ShelleyAddress(
            "stake178phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtcccycj5"
        )
        self.assertEqual(addr.hrp, "stake")
        self.assertEqual(addr.network_tag, NetworkTag.MAINNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_testnet_PaymentKeyHash_StakeKeyHash(self):
        addr = ShelleyAddress(
            "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_testnet_ScriptHash_StakeKeyHash(self):
        addr = ShelleyAddress(
            "addr_test1zrphkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gten0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgsxj90mg"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_testnet_PaymentKeyHash_ScriptHash(self):
        addr = ShelleyAddress(
            "addr_test1yz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzerkr0vd4msrxnuwnccdxlhdjar77j6lg0wypcc9uar5d2shsf5r8qx"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_testnet_ScriptHash_ScriptHash(self):
        addr = ShelleyAddress(
            "addr_test1xrphkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gt7r0vd4msrxnuwnccdxlhdjar77j6lg0wypcc9uar5d2shs4p04xh"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Hash)

    def test_testnet_PaymentKeyHash_Pointer(self):
        addr = ShelleyAddress(
            "addr_test1gz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer5pnz75xxcrdw5vky"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHash_Pointer)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Pointer)

    def test_testnet_ScriptHash_Pointer(self):
        addr = ShelleyAddress(
            "addr_test12rphkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtupnz75xxcryqrvmw"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash_Pointer)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsInstance(addr.components[1], Pointer)

    def test_testnet_PaymentKeyHashOnly(self):
        addr = ShelleyAddress(
            "addr_test1vz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzerspjrlsz"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.PaymentKeyHashOnly)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_testnet_ScriptHashOnly(self):
        addr = ShelleyAddress(
            "addr_test1wrphkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtcl6szpr"
        )
        self.assertEqual(addr.hrp, "addr_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHashOnly)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_testnet_StakeKeyHash(self):
        addr = ShelleyAddress(
            "stake_test1uqehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gssrtvn"
        )
        self.assertEqual(addr.hrp, "stake_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.StakeKeyHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])

    def test_testnet_ScriptHash(self):
        addr = ShelleyAddress(
            "stake_test17rphkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtcljw6kf"
        )
        self.assertEqual(addr.hrp, "stake_test")
        self.assertEqual(addr.network_tag, NetworkTag.TESTNET)
        self.assertEqual(addr.address_type, AddressType.ScriptHash)
        self.assertIsInstance(addr.components[0], Hash)
        self.assertIsNone(addr.components[1])
