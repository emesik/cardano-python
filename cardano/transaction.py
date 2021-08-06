import collections
import operator

from .address import Address
from .metadata import Metadata
from .numbers import as_ada


class Transaction(object):
    """
    Represents a Cardano transaction.

    :param txid:            the ID of the transaction
    :param fee:             fee amount in ADA
    :param inputs:          a sequence of :class:`Input` objects
    :param outputs:         a sequence of :class:`Output` objects
    :param local_inputs:    a sequence of :class:`Input` objects that originate from local wallet
    :param local_outputs:   a sequence of :class:`Output` objects that are destined to local wallet
    :param withdrawals:     a sequence of (:class:`Decimal`, :class:`str`) pairs of amounts and
                            stake addresses
    :param metadata:        an instance of :class:`Metadata <cardano.metadata.Metadata>`
    """

    txid = None
    fee = None
    inputs = None
    outputs = None
    local_inputs = None
    local_outputs = None
    withdrawals = None
    inserted_at = None
    expires_at = None
    pending_since = None
    metadata = None

    def __init__(self, txid=None, **kwargs):
        self.txid = txid or self.txid
        fee = kwargs.pop("fee", None)
        self.fee = fee if fee is not None else self.fee
        self.inputs = kwargs.pop("inputs", []) or (
            self.inputs if self.inputs is not None else []
        )
        self.outputs = kwargs.pop("outputs", []) or (
            self.outputs if self.outputs is not None else []
        )
        self.local_inputs = kwargs.pop("local_inputs", []) or (
            self.local_inputs if self.local_inputs is not None else []
        )
        self.local_outputs = kwargs.pop("local_outputs", []) or (
            self.local_outputs if self.local_outputs is not None else []
        )
        self.withdrawals = kwargs.pop("withdrawals", []) or (
            self.withdrawals if self.withdrawals is not None else []
        )
        self.inserted_at = kwargs.pop("inserted_at", None) or self.inserted_at
        self.expires_at = kwargs.pop("expires_at", None) or self.expires_at
        self.pending_since = kwargs.pop("pending_since", None) or self.pending_since
        self.metadata = kwargs.pop("metadata", Metadata()) or (
            self.metadata if self.metadata is not None else Metadata()
        )

    @property
    def local_inputs_sum(self):
        return as_ada(sum(map(operator.attrgetter("amount"), self.local_inputs)))

    @property
    def local_outputs_sum(self):
        return as_ada(sum(map(operator.attrgetter("amount"), self.local_outputs)))

    @property
    def amount_in(self):
        return as_ada(max(0, self.local_outputs_sum - self.local_inputs_sum))

    @property
    def amount_out(self):
        return as_ada(
            max(
                0,
                self.local_inputs_sum - self.local_outputs_sum - self.fee
                if self.fee is not None
                else 0,
            )
        )

#    @property
#    def assets(self):
#        _assets = collections.defaultdict(int)
#        print("i")
#        for inp in self.inputs:
#            print(inp.assets)
#            for aid, aqty in inp.assets:
#                _assets[aid] += -aqty if inp in self.local_inputs else aqty
#                print(dict(_assets))
#        print("o")
#        for outp in self.outputs:
#            print(outp.assets)
#            for aid, aqty in outp.assets:
#                print(outp in self.local_outputs)
#                _assets[aid] += aqty if outp in self.local_outputs else -aqty
#                print(dict(_assets))
#        return dict(_assets)

    def hash(self):
        return self.txid


class IOBase(object):
    def __init__(self, address=None, amount=None, assets=None):
        self.address = None if address is None else Address(address)
        self.amount = amount
        self.assets = assets or []


class Input(IOBase):
    """
    Represents a :class:`Transaction` input.

    :param iid:     the input ID
    :type iid:      :class:`str` hex
    :param address: the origin address
    :type address:  :class:`cardano.address.Address`
    :param amount:  the amount in ADA
    :type amount:   :class:`Decimal`
    :param assets:  a sequence of :class:`AssetID <cardano.simpletypes.AssetID>` quantity pairs
    :type assets:   :class:`list`
    """

    def __init__(self, iid=None, address=None, amount=None, assets=None):
        super(Input, self).__init__(address=address, amount=amount, assets=assets)
        self.id = iid


class Output(IOBase):
    """
    Represents a :class:`Transaction` output.

    :param address: the destination address
    :type address:  :class:`cardano.address.Address`
    :param amount:  the amount in ADA
    :type amount:   :class:`Decimal`
    :param assets:  a sequence of :class:`AssetID <cardano.simpletypes.AssetID>` quantity pairs
    :type assets:   :class:`list`
    """

    pass
