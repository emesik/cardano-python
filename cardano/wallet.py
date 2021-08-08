from .address import Address
from .simpletypes import StakePoolInfo
from .transaction import TransactionManager
from . import exceptions


class WalletService(object):
    """
    Represents the service responsible for listing and retrieving the existing wallets or creating
    new ones.

    :param backend: the backend used to handle the underlying service layer

    """

    def __init__(self, backend=None):
        self.backend = backend

    def wallets(self):
        """
        Returns the list of all :class:`Wallets <Wallet>` handled by the backend.
        """
        return [Wallet(wid, backend=self.backend) for wid in self.backend.wallet_ids()]

    def wallet(self, wid, passphrase=None):
        """
        Returns the wallet of given ID, connected to the backend and equipped with the passphrase
        if given.

        :param wid:             The wallet ID (hex string)
        :param passphrase:      The wallet passphrase for spending operations (plain text string)
        :rtype:                 :class:`Wallet`
        """
        return Wallet(wid, backend=self.backend, passphrase=passphrase)

    def create_wallet(self, name, mnemonic, passphrase, mnemonic_2f=None):
        """
        Creates/restores a wallet internally in the backend.
        Returns only ID as the backend may need some time to sync before being able to return
        full wallet data.

        :param name:            Name of the wallet
        :param mnemonic:        The mnemonic seed
        :param passphrase:      The wallet passphrase for spending operations (plain text string)
        :param mnemonic_2f:     An optional passphrase used to encrypt the mnemonic sentence
        :rtype:                 :class:`str`
        """
        return self.backend.create_wallet(name, mnemonic, passphrase, mnemonic_2f)


class Wallet(object):
    """
    Represents a single wallet. Allows for browsing the history, checking balance and spending
    funds.

    :param wid:         the wallet ID
    :param backend:     the backend used to handle the underlying service layer
    :param passphrase:  the passphrase protecting the wallet's spending functionality, not required
                        for read-only operations. It will be stored for the entire lifetime of the
                        object in ``.passphrase`` field. It might be also provided for each
                        individual spend operation, then it will be discarded after use.
    """

    passphrase = None

    def __init__(self, wid, backend, passphrase=None):
        self.wid = wid
        self.backend = backend
        self.passphrase = passphrase or self.passphrase
        if not self.backend.wallet_exists(wid):
            raise ValueError("Wallet of id '{:s}' doesn't exist.".format(wid))
        self.transactions = TransactionManager(self.wid, self.backend)

    def sync_progress(self):
        """
        Returns the progress of synchronization with the blockchain. The value is :class:`float`
        ranging from ``0.0`` to ``1.0``.
        """
        return self.backend.sync_progress(self.wid)

    def addresses(self, with_usage=False):
        """
        Returns full list of already generated addresses.

        :param with_usage:  A :class:`bool` indicating whether to retrieve used/unused address
                            status too.
        :rtype:     :class:`list` of :class:`Address <cardano.address.Address>` objects when
                    ``with_usage == False`` and of (:class:`Address <cardano.address.address>`,
                    :class:`bool`) tuples otherwise.
        """
        if with_usage:
            return [
                (Address(addr[0], wallet=self), addr[1])
                for addr in self.backend.addresses(self.wid)
            ]
        return [
            Address(addr[0], wallet=self) for addr in self.backend.addresses(self.wid)
        ]

    def first_unused_address(self):
        """
        Returns the first unused address. **There is no internal pointer and the result is based
        on blockchain and mempool state only, and their interpretation by the backend**,
        so multiple subsequent calls will return the same address if no transfer is received
        between them.
        """
        return next(filter(lambda a: not a[1], self.addresses(with_usage=True)))[1]

    def balance(self):
        """
        Returns the :class:`Balance <cardano.simpletypes.Balance>` of the wallet.
        """
        return self.backend.balance(self.wid)

    def assets(self):
        """
        Returns the balance of native assets.

        :rtype:     :class:`dict` of :class:`AssetID`: :class:`Balance <cardano.simpletypes.Balance>` pairs
        """
        return self.backend.asset_balances(self.wid)

    def delete(self):
        """
        Deletes the wallet from the backend. It doesn't wipe the funds; the wallet may be restored
        later on, using the mnemonic phrase.
        """
        return self.backend.delete_wallet(self.wid)

    def _resolve_passphrase(self, passphrase):
        passphrase = passphrase or self.passphrase
        if passphrase is None:
            raise exceptions.MissingPassphrase(
                "Cannot perform operation without the passphrase"
            )
        return passphrase

    def transfer(
        self,
        address,
        amount,
        assets=None,
        metadata=None,
        allow_withdrawal=True,
        ttl=None,
        passphrase=None,
    ):
        """
        Sends a transfer from the wallet. Returns the resulting transaction.

        :param address: destination :class:`Address <cardano.address.Address>` or subtype
        :param amount: amount to send
        :param assets: a sequence of :class:`AssetID <cardano.simpletypes.AssetID>` and quantity
                    pairs
        :param metadata: metadata to be sent, as :class:`Metadata <cardano.metadata.Metadata>`
                    instance od ``dict`` mapping ``int`` keys to values of acceptable types
        :param allow_withdrawal: Allow withdrawing staking rewards to cover the transaction amount
                    or fee.
        :param ttl: Time To Live in seconds. After TTL has lapsed the nodes give up on broadcasting
                    the transaction. Leave `None` to use the default value.
        :param passphrase: the passphrase to the wallet. It takes precedence over `self.passphrase`
                    and is discarded after use. If neither `self.passphrase` nor `passphrase` is
                    set, a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                    exception will be raised.
        :rtype: :class:`Transaction <cardano.transaction.Transaction>`
        """
        return self.backend.transfer(
            self.wid,
            ((address, amount, assets or []),),
            metadata,
            allow_withdrawal,
            ttl,
            self._resolve_passphrase(passphrase),
        )

    def transfer_multiple(
        self,
        destinations,
        metadata=None,
        allow_withdrawal=True,
        ttl=None,
        passphrase=None,
    ):
        """
        Sends multiple transfers from the wallet. Returns the resulting transaction.

        :param destinations: a list of :class:`Address <cardano.address.Address>` and amount
                    pairs ``[(address, amount), ...]``
        :param metadata: metadata to be sent, as :class:`Metadata <cardano.metadata.Metadata>`
                    instance od ``dict`` mapping ``int`` keys to values of acceptable types
        :param allow_withdrawal: Allow withdrawing staking rewards to cover the transaction amount
                    or fee.
        :param ttl: Time To Live in seconds. After TTL has lapsed the nodes give up on broadcasting
                    the transaction. Leave `None` to use the default value.
        :param passphrase: the passphrase to the wallet. It takes precedence over `self.passphrase`
                    and is discarded after use. If neither `self.passphrase` nor `passphrase` is
                    set, a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                    exception will be raised.
        :rtype: :class:`Transaction <cardano.transaction.Transaction>`
        """
        dests = []
        for d in destinations:
            nd = d if len(d) == 3 else (d[0], d[1], [])
            dests.append(nd)
        return self.backend.transfer(
            self.wid,
            dests,
            metadata,
            allow_withdrawal,
            ttl,
            self._resolve_passphrase(passphrase),
        )

    def estimate_fee(self, destinations, metadata=None):
        """
        Estimates the fee for a potential transaction to specified destinations and carrying
        optional metadata. Returns a tuple of estimated minimum and maximum fee, in ADA.

        :param destinations: a list of :class:`Address <cardano.address.Address>` and amount
                    pairs ``[(address, amount), ...]``
        :param metadata: metadata to be sent, as :class:`Metadata <cardano.metadata.Metadata>`
                    instance od ``dict`` mapping ``int`` keys to values of acceptable types
        :rtype: (``Decimal``, ``Decimal``)
        """
        return self.backend.estimate_fee(self.wid, destinations, metadata)

    def stake_pools(self, stake=None):
        """
        Returns a list of known stake pools ordered by descending rewards.

        :param stake:   The amount of ADA to be staked. Optional. If omitted, the wallet's total
                        balance will be used instead.
        :type stake:    :class:`Decimal`
        :rtype:         :class:`list`
        """
        return self.backend.stake_pools(
            self.wid, stake if stake is not None else self.balance().total
        )

    def staking_status(self):
        """
        Returns information about staking status.

        :rtype:         :class:`StakingStatus <cardano.simpletypes.StakingStatus>`
        """
        return self.backend.staking_status(self.wid)

    def stake(self, pool, passphrase=None):
        """
        Stakes all wallet balance at the given pool.

        :param pool:        The pool to stake ADA at
        :type stake:        Pool ID as hex :class:`str`
                            or :class:`StakePoolInfo <cardano.simpletypes.StakePoolInfo>`
        :param passphrase:  the passphrase to the wallet. It takes precedence over `self.passphrase`
                            and is discarded after use. If neither `self.passphrase` nor
                            `passphrase` is set,
                            a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                            exception will be raised.
        :rtype:             :class:`Transaction <cardano.transaction.Transaction>`
        """
        pool_id = pool.id if isinstance(pool, StakePoolInfo) else pool
        return self.backend.stake(
            self.wid, pool_id, self._resolve_passphrase(passphrase)
        )

    def unstake(self, passphrase=None):
        """
        Cancels active stake delegation.

        :param passphrase:  the passphrase to the wallet. It takes precedence over `self.passphrase`
                            and is discarded after use. If neither `self.passphrase` nor
                            `passphrase` is set,
                            a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                            exception will be raised.
        :rtype:             :class:`Transaction <cardano.transaction.Transaction>`
        """
        return self.backend.unstake(self.wid, self._resolve_passphrase(passphrase))

    def utxo_stats(self):
        """
        Returns UTXO statistics as a tuple of ``(total_balance, histogram, scale)``.
        """
        return self.backend.utxo_stats(self.wid)
