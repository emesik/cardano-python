from .address import Address


class Transaction(object):
    txid = None

    def __init__(self, txid, **kwargs):
        self.txid = txid
        self.amount = kwargs.pop("amount")
        self.fee = kwargs.pop("fee")
        self.inputs = kwargs.pop("inputs")
        self.outputs = kwargs.pop("outputs")


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
