import collections
import operator
import re
import warnings

from .address import Address, address
from .metadata import Metadata
from .numbers import as_ada

__all__ = ("Transaction", "Input", "Output", "validate_txid")


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
    status = None
    metadata = None

    def __init__(self, txid=None, **kwargs):
        self.txid = txid or self.txid
        validate_txid(self.txid)
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
        self.status = kwargs.pop("status", None) or self.status
        self.metadata = kwargs.pop("metadata", Metadata()) or (
            self.metadata if self.metadata is not None else Metadata()
        )

    def __repr__(self):
        return "<Cardano tx: {:s}>".format(self.txid)

    def __format__(self, spec):
        return format(str(self), spec)

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


def validate_txid(txid):
    if not bool(re.compile("^[0-9a-f]{64}$").match(txid)):
        raise ValueError(
            "Transaction ID must be a 64-character hexadecimal string, not "
            "'{}'".format(txid)
        )
    return txid


class TransactionManager(object):
    wid = None
    backend = None

    def __init__(self, wid, backend):
        self.wid = wid
        self.backend = backend

    def __call__(self, **filterparams):
        filter_ = TxFilter(**filterparams)
        return filter_.filter(self.backend.transactions(self.wid))


class _ByHeight(object):
    """A helper class used as key in sorting of payments by height.
    Mempool goes on top, blockchain payments are ordered with descending block numbers.

    **WARNING:** Integer sorting is reversed here.
    """

    def __init__(self, tx):
        self.tx = tx

    def _cmp(self, other):
        sh = self.tx.inserted_at
        oh = other.tx.inserted_at
        if sh is oh is None:
            return 0
        if sh is None:
            return 1
        if oh is None:
            return -1
        return (sh.absolute_slot > oh.absolute_slot) - (
            sh.absolute_slot < oh.absolute_slot
        )

    def __lt__(self, other):
        return self._cmp(other) > 0

    def __le__(self, other):
        return self._cmp(other) >= 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ge__(self, other):
        return self._cmp(other) <= 0

    def __gt__(self, other):
        return self._cmp(other) < 0

    def __ne__(self, other):
        return self._cmp(other) != 0


class TxFilter(object):
    #
    # Available filters:
    # - txid
    # - src_addr
    # - dest_addr
    # - min_epoch
    # - max_epoch
    # - min_slot
    # - max_slot
    # - min_height
    # - max_height
    # - confirmed
    # - unconfirmed
    #
    def __init__(self, **filterparams):
        self.min_epoch = filterparams.pop("min_epoch", None)
        self.max_epoch = filterparams.pop("max_epoch", None)
        self.min_slot = filterparams.pop("min_slot", None)
        self.max_slot = filterparams.pop("max_slot", None)
        self.min_absolute_slot = filterparams.pop("min_absolute_slot", None)
        self.max_absolute_slot = filterparams.pop("max_absolute_slot", None)
        self.min_height = filterparams.pop("min_height", None)
        self.max_height = filterparams.pop("max_height", None)
        self.unconfirmed = filterparams.pop("unconfirmed", False)
        self.confirmed = filterparams.pop("confirmed", True)
        _txid = filterparams.pop("txid", None)
        _src_addr = filterparams.pop("src_addr", None)
        _dest_addr = filterparams.pop("dest_addr", None)
        if len(filterparams) > 0:
            raise ValueError(
                "Excessive arguments for payment query: {}".format(filterparams)
            )
        self._asks_chain_position = any(
            map(
                lambda x: x is not None,
                (
                    self.min_epoch,
                    self.max_epoch,
                    self.min_slot,
                    self.max_slot,
                    self.min_absolute_slot,
                    self.max_absolute_slot,
                    self.min_height,
                    self.max_height,
                ),
            )
        )
        if self.unconfirmed and self._asks_chain_position:
            warnings.warn(
                "Blockchain position filtering ({max,min}_{epoch,slot,block}) has been "
                "requested while also asking for transactions not in ledger. "
                "These are mutually exclusive. "
                "As mempool transactions have no height at all, they will be excluded "
                "from the result.",
                RuntimeWarning,
            )
        self.src_addrs = self._get_addrset(_src_addr)
        self.dest_addrs = self._get_addrset(_dest_addr)
        if _txid is None:
            self.txids = []
        else:
            if isinstance(_txid, (bytes, str)):
                txids = [_txid]
            else:
                iter(_txid)
                txids = _txid
            self.txids = list(map(validate_txid, txids))

    def _get_addrset(self, addr):
        if addr is None:
            return set()
        else:
            if isinstance(addr, (str, bytes)):
                addrs = [addr]
            else:
                try:
                    iter(addr)
                    addrs = addr
                except TypeError:
                    addrs = [addr]
            return set(map(address, addrs))

    def check(self, tx):
        assert (tx.status == "in_ledger" and tx.inserted_at is not None) or (
            tx.status != "in_ledger" and tx.inserted_at is None
        )
        ht = tx.inserted_at
        if ht is None:
            if not self.unconfirmed:
                return False
            if self._asks_chain_position:
                # mempool txns are filtered out if any height range check is present
                return False
        else:
            if not self.confirmed:
                return False
            if self.min_epoch is not None and ht.epoch < self.min_epoch:
                return False
            if self.max_epoch is not None and ht.epoch > self.max_epoch:
                return False
            if self.min_slot is not None and ht.slot < self.min_slot:
                return False
            if self.max_slot is not None and ht.slot > self.max_slot:
                return False
            if (
                self.min_absolute_slot is not None
                and ht.absolute_slot < self.min_absolute_slot
            ):
                return False
            if (
                self.max_absolute_slot is not None
                and ht.absolute_slot > self.max_absolute_slot
            ):
                return False
            if self.min_height is not None and ht.height < self.min_height:
                return False
            if self.max_height is not None and ht.height > self.max_height:
                return False
        if self.txids and tx.txid not in self.txids:
            return False
        srcs = set(filter(None, map(operator.attrgetter("address"), tx.inputs)))
        dests = set(filter(None, map(operator.attrgetter("address"), tx.inputs)))
        if self.src_addrs and not self.src_addrs.intersection(srcs):
            return False
        if self.dest_addrs and not self.dest_addrs.intersection(dests):
            return False
        return True

    def filter(self, txns):
        return sorted(filter(self.check, txns), key=_ByHeight)
