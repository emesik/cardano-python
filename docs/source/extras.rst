UTXO stats
==========

The :class:`Wallet <cardano.wallet.Wallet>` has a ``utxo_stats()`` method which
returns a histogram of :abbr:`UTXO (Unspent Transaction Output)` statistics.

The result consists of three elements: total balance, histogram, scale.

The histogram part is a list of ``(threshold, number)`` pairs where the number
describes how many UTXOs are available between the given threshold and the lower one.

The scale so far is always ``"log10"``.

.. code-block:: python

    In [40]: total, dist, scale = wallet.utxo_stats()

    In [41]: total
    Out[41]: Decimal('1052.422864')

    In [42]: scale
    Out[42]: 'log10'

    In [43]: print("\n".join(["{:18.6f}: {:4d}".format(*d) for d in dist.items()]))
              0.000010:    0
              0.000100:    0
              0.001000:    0
              0.010000:    0
              0.100000:    0
              1.000000:    1
             10.000000:   16
            100.000000:    0
           1000.000000:    2
          10000.000000:    0
         100000.000000:    0
        1000000.000000:    0
       10000000.000000:    0
      100000000.000000:    0
     1000000000.000000:    0
    10000000000.000000:    0
    45000000000.000000:    0
