from .consts import Era


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
    if (
        addr.startswith("addr1")
        or addr.startswith("addr_test1")
        or addr.startswith("stake1")
        or addr.startswith("stake_test1")
    ):
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


class IcarusAddress(ByronAddress):
    pass


class ShelleyAddress(Address):
    era = Era.SHELLEY
