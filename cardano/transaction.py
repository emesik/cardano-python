from .address import Address


class Transaction(object):
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
    def __init__(self, iid=None, address=None, amount=None):
        super(Input, self).__init__(address=address, amount=amount)
        self.id = iid


class Output(IOBase):
    pass
