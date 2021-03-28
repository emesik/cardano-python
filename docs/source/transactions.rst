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

API reference
-------------

.. automodule:: cardano.transaction
   :members:
