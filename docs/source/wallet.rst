Working with wallets
====================

The example presented in the :doc:`quickstart section <quickstart>` will certainly fail in your
environment, as you don't have the same wallet created yet. In order to set up a new wallet, you
need to learn first about two kinds of objects:

1. ``Wallet`` which represents a single Cardano wallet and allows for operations like balance
   retrieval, searching through the transaction history and spending funds.
   Wallets are identified by unique ID which is deterministically derived from the seed (mnemonic
   phrase), so each time you delete and create a wallet again, it receives the same ID.

2. ``WalletService`` which is responsible for creating new and listing or retrieving existing
   wallets.

3. Backend, which represents the underlying service layer. At the moment the only backend
   available is the REST API provided by ``cardano-wallet``, represented by the ``WalletREST``
   objects.

.. note:: Remember that creating or deleting a wallet will not record any information on the
    blockchain. If the wallet you're creating existed before, you'll be presented its' entire
    history. Likweise, if you delete a wallet, you'll be able to create it again in this or any
    other software and claim the funds or see historical transactions.

Creating wallets
----------------

Let's assume your backend doesn't know anything about the wallet
``eff9cc89621111677a501493ace8c3f05608c0ce``, which is exactly your starting scenario. In order
to obtain that wallet object, you'd have first to create it:

.. code-block:: python

    In [1]: from cardano.wallet import WalletService

    In [2]: from cardano.backends.walletrest import WalletREST

    In [3]: ws = WalletService(WalletREST(port=8090))

    In [4]: wal = ws.create_wallet(
            name="test wallet",
            mnemonic="resist render west spin antique wild gossip thing syrup network risk gospel seek drop receive",
            passphrase="xxx",
            )

    In [4]: wal.sync_progress()
    Out[4]: 0.05

    In [5]: wal.balance()
    Out[5]: Balance(total=Decimal('0.000000'), available=Decimal('0.000000'), reward=Decimal('0.000000'))

Even though this wallet may contain some funds (on *testnet*), right after creation the balance
will be null and the transaction history empty. This is because of ongoing sync process which scans
the entire blockchain for transaction history.

Balance tuple
~~~~~~~~~~~~~

The balance returned by ``wal.balance()`` (as well as balances of native assets) is a subclass of
``collections.namedtuple``. It consists of three elements:

0. ``total`` — indicating the total amount of funds in the wallet, without going into too much
    details.
1. ``available`` — the amount of funds without staking rewards, might be also considered as the
    principal paid to the wallet and used for staking.
2. ``reward`` — the amount received as staking interest.

Hence, to just get the full balance, you may use ``wal.balance().total``.

Sync progress
~~~~~~~~~~~~~

The value returned by ``.sync_progress()`` is a float number that represents how advanced the
synchronization process is. It starts from ``0.0`` and goes up to ``1.0`` which says the wallet is
up to date with the blockchain. A simple synchronization wait loop might look like the following:

.. code-block:: python

    In [6]: import time

    In [7]: while wal.sync_progress() < 1.0:
                time.sleep(1)

Depending on your conditions, you may use other sleep period value. Just remember to call it within
the loop, as it releases CPU time to other processes instead of constantly bombarding your REST API
with requests.

Retrieving existing wallets
---------------------------

In case your backend already knows about the wallet, you may use much simpler approach:

.. code-block:: python

    In [1]: from cardano.wallet import Wallet

    In [2]: from cardano.backends.walletrest import WalletREST

    In [3]: wal = Wallet("eff9cc89621111677a501493ace8c3f05608c0ce", backend=WalletREST(port=8090))

    In [4]: wal.sync_progress()
    Out[4]: 1.0

    In [5]: wal.balance()
    Out[5]: Balance(total=Decimal('998.831199'), available=Decimal('998.831199'), reward=Decimal('0.000000'))

.. note:: Although the backend is a required argument right now, the example passes it to the
    contstructor like it was optional. This is because in the near future some offline
    functionality will be added to the ``Wallet`` class and initialization without backend will be
    available.


Removing wallets
----------------

This is a trivial operation:

.. code-block:: python

    In [6]: wal.delete()

After that, if you try to use the wallet object again, the
:class:`cardano.backends.walletrest.exceptions.NotFound` exception will be raised.

API reference
-------------

.. automodule:: cardano.wallet
   :members:
