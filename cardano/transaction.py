from .address import Address


class Transaction(object):
    """
    Represents a Cardano transaction.

    :param txid:            the ID of the transaction
    :param gross_amount:    gross amount, consisting of the amount of ADA paid and the fee
    :param fee:             fee amount in ADA
    :param inputs:          a sequence of :class:`Input` objects
    :param outputs:         a sequence of :class:`Output` objects
    :param direction:       either ``"incoming"`` or ``"outgoing"``
    """
    txid = None
    gross_amount = None
    fee = None
    inputs = None
    outputs = None
    direction = None
    inserted_at = None
    expires_at = None
    pending_since = None

    def __init__(self, txid=None, **kwargs):
        self.txid = txid or self.txid
        gross_amount = kwargs.pop("gross_amount", None)
        self.gross_amount = gross_amount if gross_amount is not None else self.gross_amount
        fee = kwargs.pop("fee", None)
        self.fee = fee if fee is not None else self.fee
        self.inputs = kwargs.pop("inputs", None) or self.inputs if self.inputs is not None else []
        self.outputs = kwargs.pop("outputs", None) or self.outputs if self.outputs is not None else []
        self.direction = kwargs.pop("direction", None) or self.direction
        self.inserted_at = kwargs.pop("inserted_at", None) or self.inserted_at
        self.expires_at = kwargs.pop("expires_at", None) or self.expires_at
        self.pending_since = kwargs.pop("pending_since", None) or self.pending_since

    @property
    def amount(self):
        return self.gross_amount - self.fee


class IOBase(object):
    def __init__(self, address=None, amount=None):
        self.address = None if address is None else Address(address)
        self.amount = amount


class Input(IOBase):
    """
    Represents a :class:`Transaction` input.

    :param address: the origin address
    :type address:  :class:`cardano.address.Address`
    :param amount:  the amount in ADA
    :type amount:   :class:`Decimal`
    """
    def __init__(self, iid=None, address=None, amount=None):
        super(Input, self).__init__(address=address, amount=amount)
        self.id = iid


class Output(IOBase):
    """
    Represents a :class:`Transaction` output.

    :param address: the destination address
    :type address:  :class:`cardano.address.Address`
    :param amount:  the amount in ADA
    :type amount:   :class:`Decimal`
    """
    pass
