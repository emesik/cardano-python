from binascii import hexlify
import enum
import re

from . import bech32

PREFIXES = [
    "addr",
    "addr_test",
    "script",
    "stake",
    "stake_test"
    #      -- * Hashes
    ,
    "addr_vkh",
    "stake_vkh",
    "addr_shared_vkh",
    "stake_shared_vkh"
    #      -- * Keys for 1852H
    ,
    "addr_vk",
    "addr_sk",
    "addr_xvk",
    "addr_xsk",
    "acct_vk",
    "acct_sk",
    "acct_xvk",
    "acct_xsk",
    "root_vk",
    "root_sk",
    "root_xvk",
    "root_xsk",
    "stake_vk",
    "stake_sk",
    "stake_xvk",
    "stake_xsk"
    #      -- * Keys for 1854H
    ,
    "addr_shared_vk",
    "addr_shared_sk",
    "addr_shared_xvk",
    "addr_shared_xsk",
    "acct_shared_vk",
    "acct_shared_sk",
    "acct_shared_xvk",
    "acct_shared_xsk",
    "root_shared_vk",
    "root_shared_sk",
    "root_shared_xvk",
    "root_shared_xsk",
    "stake_shared_vk",
    "stake_shared_sk",
    "stake_shared_xvk",
    "stake_shared_xsk",
]

SHELLEY_ADDR_RE = re.compile("^(" + "|".join(PREFIXES) + ")")


class NetworkTag(enum.IntEnum):
    TESTNET = 0
    MAINNET = 1


class AddressType(enum.IntEnum):
    PaymentKeyHash_StakeKeyHash = 0
    ScriptHash_StakeKeyHash = 1
    PaymentKeyHash_ScriptHash = 2
    ScriptHash_ScriptHash = 3
    PaymentKeyHash_Pointer = 4
    ScriptHash_Pointer = 5
    PaymentKeyHashOnly = 6
    ScriptHashOnly = 7
    StakeKeyHash = 0xE
    ScriptHash = 0xF


class Hash(object):
    hex_repr = None

    def __init__(self, data):
        if len(data) != 28:
            raise ValueError(
                "Hash object needs 28 bytes, {:d} provided".format(len(data))
            )
        self.hex_repr = hexlify(bytes(data)).decode()

    def __str__(self):
        return self.hex_repr


class Pointer(object):
    absolute_slot = 0
    tx_index = None
    output_index = None

    def __init__(self, data):
        data = data.copy()
        self.absolute_slot, data = self._popint(data)
        self.tx_index, data = self._popint(data)
        self.output_index, data = self._popint(data)

    def _popint(self, data):
        _intbytes = []
        while data:
            b = data[0]
            data = data[1:]
            _intbytes.append(b & 0x7F)
            if b & 0x80 == 0:
                break
        val = 0
        for idx, b in enumerate(reversed(_intbytes)):
            val = val | (b << (8 * idx) - idx)
        return val, data


class AddressDeserializer(object):
    ADDR_LENGTH_CHECK = {
        AddressType.PaymentKeyHash_StakeKeyHash: lambda l: l == 28 * 2,
        AddressType.ScriptHash_StakeKeyHash: lambda l: l == 28 * 2,
        AddressType.PaymentKeyHash_ScriptHash: lambda l: l == 28 * 2,
        AddressType.ScriptHash_ScriptHash: lambda l: l == 28 * 2,
        AddressType.PaymentKeyHash_Pointer: lambda l: l > 28,
        AddressType.ScriptHash_Pointer: lambda l: l > 28,
        AddressType.PaymentKeyHashOnly: lambda l: l == 28,
        AddressType.ScriptHashOnly: lambda l: l == 28,
        AddressType.StakeKeyHash: lambda l: l == 28,
        AddressType.ScriptHash: lambda l: l == 28,
    }
    network_tag = None
    address_type = None
    components = None
    hrp = None
    payload = None

    def __init__(self, address):
        """
        Performs basic validation of a Shelley address but doesn't analyze the payload.

        :param addres:      a Shelley address as a :class:`str`
        """
        self.hrp, binaddr5bit = bech32.bech32_decode(address)
        if not binaddr5bit:
            raise ValueError("{:s} is not a valid Shelley address".format(address))
        binaddr = bech32.convertbits(binaddr5bit, 5, 8, False)
        header = binaddr[0]
        self.payload = binaddr[1:]
        self.address_type, self.network_tag = (header & 0xF0) >> 4, header & 0xF
        if self.address_type not in AddressType.__members__.values():
            raise ValueError(
                "Shelley address {:s} is of wrong type (0x{:x})".format(
                    address, self.address_type
                )
            )
        if self.network_tag not in NetworkTag.__members__.values():
            raise ValueError(
                "Shelley address {:s} has unsupported net tag (0x{:x})".format(
                    address, self.network_tag
                )
            )
        if self.network_tag == NetworkTag.TESTNET and not self.hrp.endswith("_test"):
            raise ValueError(
                'Shelley address {:s} has TESTNET tag but the prefix doesn\'t end with "_test"'.format(
                    address
                )
            )
        elif self.network_tag == NetworkTag.MAINNET and self.hrp.endswith("_test"):
            raise ValueError(
                'Shelley address {:s} has MAINNET tag but the prefix ends with "_test"'.format(
                    address
                )
            )
        if not self.ADDR_LENGTH_CHECK[self.address_type](len(self.payload)):
            raise ValueError(
                "Shelley address {:s} has invalid self.payload length".format(address)
            )

    def deserialized(self):
        """
        Returns data deserialized from the address.

        :rtype: (:class:`NetworkTag`, :class:`AddressType`, :class:`list` of :class:`AddressComponents <AddressComponent>`)
        """
        part1, part2 = Hash(self.payload[:28]), self.payload[28:]
        if self.address_type in (
            AddressType.PaymentKeyHash_Pointer,
            AddressType.ScriptHash_Pointer,
        ):
            part2 = Pointer(part2) if part2 else None
        else:
            part2 = Hash(part2) if part2 else None
        self.components = (part1, part2)
        return (self.hrp, self.network_tag, self.address_type, self.components)
