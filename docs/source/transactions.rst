Listing transactions and spending funds
=======================================

From wallet perspective transactions can be generally grouped into incoming and outgoing. This is
just a convenience, as almost every outgoing transaction has a change amount that goes back to the
originating wallet.

Listing transactions
--------------------

Retrieving the history of the wallet is pretty straightforward:

.. code-block:: python

    In [8]: txns = wal.transactions()

    In [9]: txns[0].txid
    Out[9]: '88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c'

    In [10]: txns[0].amount_out
    Out[10]: Decimal('1.000000')

    In [11]: txns[0].fee
    Out[11]: Decimal('0.168801')

    In [12]: txns[1].txid
    Out[12]: '0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264'

As you probably noticed, the amounts are given in ADA as Python ``Decimal`` type, which is perfect
for monetary operations.

Narrowing down the query
~~~~~~~~~~~~~~~~~~~~~~~~

In order to limit the number of results you may ask for transactions meeting special criteria.

The most important, perhaps, is the ``txid`` argument which accepts single IDs as well as sequences
thereof. So, both

.. code-block:: python

    wal.transactions(txid="0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264")

as well as 

.. code-block:: python

    wal.transactions(txid=[
        "0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264",
        "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"]
        )

are valid queries.

Blockchain position
...................

The transaction filter accepts parameters filtering against the position in the ledger.
``min_epoch``, ``max_epoch``, ``min_slot``, ``max_slot``, ``min_absolute_slot``,
``max_absolute_slot``, ``min_height`` and ``max_height`` can be used and combined.

Ranges combining different criteria may be applied in the same call, e.g. to ask only for the
first 10 slots of epoch 230 would be

.. code-block:: python

    wal.transactions(min_epoch=230, max_epoch=230, max_slot=10)

Because both epochs and slots are precisely defined periods of time, querying for them
is like asking for quite precise timestamp of mining of the transaction's block. In contrast,
asking for height considers the actual number of blocks since the genesis, as not all slots
have been used to generate a block.

Mempool
.......

Even though the mempool life part of Cardano transactions is usually very short, it is possible to
ask for transactions not in ledger, as well as to exclude them from the results.

To include mempool, use ``unconfirmed=True``. To include mined transactions, use
``confirmed=True``. ``False`` values exclude these types of transactions from the results.

By default, ``unconfirmed=False`` and ``confirmed=True`` which means the default settings ask only
for transactions in the ledger.

Filtering by address
....................

Arguments ``src_addr`` and ``dest_addr`` filter for source and destination addresses, respectively.
They can be used to ask for single or multiple addresses, just like ``txid`` described above.

.. note:: Please be aware that this kind of query is not very reliable. ``cardano-wallet`` is known
    to return incomplete input/output data, missing the address info.

Spending funds
--------------

In order to spend funds, you need to specify the destination address, amount (as ``Decimal`` or
``int``) and provide the passphrase if you haven't done so when initializing the ``Wallet`` object.

.. code-block:: python

    In [17]: tx = wal.transfer(
        "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
        7,
        passphrase="xxx")

    In [18]: tx.txid
    Out[18]: 'a7a16a0653a6a397eb822ff8a3f610b5dabc82c5da2425fcc267f983f0edec88'

    In [19]: tx.amount_in
    Out[19]: Decimal('0.000000')

    In [20]: tx.amount_out
    Out[20]: Decimal('7.000000')

    In [21]: tx.fee
    Out[21]: Decimal('0.168801')

Another useful function is ``Wallet.transfer_multiple`` which accepts more than one destination for
a single transaction. It is useful for aggregating payouts and reducing fee costs. The difference
from the previous method is that it accepts a sequence of ``(address, amount)`` pairs.

.. code-block:: python

    In [23]: tx = wallet.transfer_multiple(
            (
                (
                    "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                    Decimal("1.234567"),
                ),
                (
                    "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                    Decimal("2.345678"),
                ),
            ),
            passphrase="xxx",
        )

    In [24]: tx.txid
    Out[24]: 'a7a16a0653a6a397eb822ff8a3f610b5dabc82c5da2425fcc267f983f0edec88'

    In [25]: tx.amount_in
    Out[25]: Decimal('0.000000')

    In [26]: tx.amount_out
    Out[26]: Decimal('3.580245')

    In [27]: tx.fee
    Out[27]: Decimal('0.168801')

Of course the list of destinations can have a single element. In fact, the ``transfer()`` method is
just a shortcut for ``transfer_multiple()`` to make single payments easier.

Estimating fees
~~~~~~~~~~~~~~~

The :class:`Wallet` object also offers method which estimates fee for transaction. The signature
is similar to ``transfer_multiple()``. It accepts a list of payments to be made and optionally the
metadata, and returns a tuple of estimated minimum and maximum fee for the eventual transaction.

.. code-block:: python

    In [23]: f = wal.estimate_fee(
            (
                ("addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                Decimal("1.234567")),
                ("addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                Decimal("2.345678")),
            ))

    In [24]: f
    Out[24]: (Decimal('0.174785'), Decimal('0.180989'))


.. note:: Don't forget to include metadata when estimating fees. They are based on the transaction
        size and additional data changes that significantly.

Metadata
--------

Since the Shelley era, Cardano allows for adding metadata to transactions. Metadata is a mapping where
keys are integers and values belong to a short list of supported data types. Description of the
structure is beyond the scope of this documentation, however you may read this `description`_ or
`another one`_ which includes a good test example.

Lists and dicts as map keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~

While Cardano supports ``map`` objects that use another ``map`` or ``list`` as key element, this
feature cannot be supported by the Python module directly. The reason is that data on blockchain is
immutable (cannot be modified) while the corresponding Python objects (``dict`` and ``list``) are
mutable, which disqualifies them as ``dict`` keys due to unstable hash value.

For that reason, substitutions have been introduced when following types of variables are used as
keys:

    * ``list``: the key on Python side is ``tuple``,
    * ``dict``: will be converted to :class:`ImmutableDict`

.. _`description`: https://github.com/input-output-hk/cardano-wallet/wiki/TxMetadata
.. _`another one`: https://github.com/input-output-hk/cardano-node/blob/master/doc/reference/tx-metadata.md

Storing and retrieving metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Metadata can be passed to ``Wallet.transfer()`` and ``Wallet.transfer_multiple()`` methods as
:class:`dict` or :class:`Metadata` instance. It will be instantly available in the ``.metadata``
attribute of the resulting :class:`Transaction` object.

.. code-block:: python

    In [23]: tx = wal.transfer(
        "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
        7,
        metadata={1: "first value", 23: "next value"},
        passphrase="xxx")

    In [24]: tx.metadata
    Out[24]: {1: 'first value', 23: 'next value'}


Metadata can be initialized separately by passing a list of ``(key, value)`` pairs.

.. code-block:: python

    In [25]: m = Metadata(((1, "first value"), (23, "next value")))

    In [26]: m
    Out[26]: {1: 'first value', 23: 'next value'}

Such instance can be also passed as ``metadata`` parameter to the transfer methods.


API reference
-------------

Transactions
~~~~~~~~~~~~

.. automodule:: cardano.transaction
   :members:

Numbers
~~~~~~~

A submodule with helpers useful for unit conversion. The idea is to represent amounts in ADA as
:class:`Decimal` type with 6 places of precision. For low-level backends, however, it's easier
to use :class:`int` of Lovelaces.

Also, :class:`float` arguments are accepted but will issue a :class:`RuntimeWarning` as it is a
**very bad idea** to use floating-point numbers for monetary data.

.. automodule:: cardano.numbers
   :members:

Metadata
~~~~~~~~

A class representing Cardano transaction metadata. Inherits from ``dict`` and offers both 
validation and serialization of the data.

.. automodule:: cardano.metadata
   :members:
