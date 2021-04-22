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

    In [10]: txns[0].amount
    Out[10]: Decimal('1.000000')

    In [11]: txns[0].fee
    Out[11]: Decimal('0.168801')

    In [12]: txns[0].gross_amount
    Out[12]: Decimal('1.168801')

    In [12]: txns[0].direction
    Out[12]: Decimal('outgoing')

    In [13]: txns[1].txid
    Out[13]: '0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264'

    In [16]: txns[1].direction
    Out[16]: 'incoming'

As you probably noticed, the amounts are given in ADA as Python ``Decimal`` type, which is perfect
for monetary operations.

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

    In [19]: tx.direction
    Out[19]: 'outgoing'

    In [20]: tx.gross_amount
    Out[20]: Decimal('7.168801')

    In [21]: tx.fee
    Out[21]: Decimal('0.168801')

    In [22]: tx.amount
    Out[22]: Decimal('7.000000')

Metadata
--------

Since the Shelley era, Cardano allows for adding metadata to transactions. Metadata is a mapping where
keys are integers and values belong to a short list of supported data types. Description of the
structure is beyond the scope of this documentation, however you may read this `description`_ or
`another one`_ which includes a good test example.

.. warning:: While Cardano supports ``map`` objects that use another ``map`` or ``list`` as key
        element, this feature is **not yet supported by the Python module**. The reason is that
        data on blockchain is immutable (cannot be modified) while the corresponding Python objects
        (``dict`` and ``list``) are mutable, which disqualifies them as ``dict`` keys.

        This is a topic for `issue #5`_ and will be resolved once a good solution has been figured
        out.

.. _`description`: https://github.com/input-output-hk/cardano-wallet/wiki/TxMetadata
.. _`another one`: https://github.com/input-output-hk/cardano-node/blob/master/doc/reference/tx-metadata.md
.. _`issue #5`: https://github.com/emesik/cardano-python/issues/5

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
