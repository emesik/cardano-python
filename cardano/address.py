class Address(object):
    _address = ""
    wallet = None

    def __init__(self, addr, wallet=None):
        self._address = addr
        self.wallet = wallet or self.wallet

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


class ByronAddress(Address):
    pass


class ShelleyAddress(Address):
    pass


def address(addr, wallet=None):
    """
    Returns an instance of proper `Address` subclass for given string.
    """
    if addr.startswith("Ae2") or addr.startswith("DdzFF"):
        return ByronAddress(addr, wallet=wallet)
    elif addr.startswith("addr1"):
        return ShelleyAddress(addr, wallet=wallet)
    raise ValueError("String {} is not a valid Cardano address")
