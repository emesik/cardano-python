import base58

from ..consts import Era
from .shelley import AddressDeserializer, SHELLEY_ADDR_RE


def address(addr, wallet=None):
    if isinstance(addr, Address):
        return addr  # already instatinated and should be of proper class
    elif isinstance(addr, (bytes, bytearray)):
        addr = addr.decode()
    elif not isinstance(addr, str):
        raise TypeError(
            "address() argument must be str, bytes, bytearray or Address instance"
        )
    # validation
    if SHELLEY_ADDR_RE.match(addr):
        AddressClass = ShelleyAddress
    elif addr.startswith("DdzFF"):
        AddressClass = ByronAddress
    elif addr.startswith("Ae2"):
        AddressClass = IcarusAddress
    else:
        raise ValueError("String {} is not a valid Cardano address".format(addr))
    return AddressClass(addr, wallet=wallet)


class Address(object):
    """
    Cardano base address class. Does no validation, it is up to child classes.

    Compares with ``str`` and ``bytes`` objects.

    :param addr:    the address as ``str`` or ``bytes`` or ``Address``
    :param wallet:  the ``Wallet`` object if address belongs to
    """

    _address = ""
    wallet = None

    def __init__(self, addr, wallet=None):
        self._address = addr
        self.wallet = wallet or self.wallet
        self._validate()

    def _validate(self):
        pass

    def __repr__(self):
        return str(self._address)

    def __eq__(self, other):
        if isinstance(other, Address):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance(other, bytes):
            return str(self).encode() == other
        return super(Address, self).__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __format__(self, spec):
        return format(str(self), spec)


class ByronAddress(Address):
    era = Era.BYRON

    def _validate(self):
        if not self._address.startswith("DdzFF"):
            raise ValueError("{:s} is not a valid Byron address".format(self._address))
        data = base58.b58decode(self._address)


class IcarusAddress(ByronAddress):
    def _validate(self):
        if not self._address.startswith("Ae2"):
            raise ValueError(
                "{:s} is not a valid Icarus/Byron address".format(self._address)
            )
        data = base58.b58decode(self._address)


class ShelleyAddress(Address):
    era = Era.SHELLEY
    network_tag = None
    address_type = None

    def _validate(self):
        (
            self.hrp,
            self.network_tag,
            self.address_type,
            self.components,
        ) = AddressDeserializer(self._address).deserialized()
