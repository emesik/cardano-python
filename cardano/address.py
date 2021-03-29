from .consts import Era


class Address(object):
    """
    Represents Cardano address. Does no validation (TBD).
    Compares with ``str`` and ``bytes`` objects.

    :param addr:    the address as ``str`` or ``bytes`` or ``Address``
    """

    _address = ""
    era = None
    wallet = None

    def __init__(self, addr, wallet=None):
        addr = addr._address if isinstance(addr, Address) else addr
        self._address = addr
        self.wallet = wallet or self.wallet
        if addr.startswith("Ae2") or addr.startswith("DdzFF"):
            self.era = Era.BYRON
        elif addr.startswith("addr1") or addr.startswith("addr_test1"):
            self.era = Era.SHELLEY
        else:
            raise ValueError("String {} is not a valid Cardano address")

    def __repr__(self):
        return self._address

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
