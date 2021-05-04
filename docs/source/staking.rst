Staking
=======

The module allows for staking ADA (also called delegation), withdrawing the stake and retrieving
information about pools. This part of the functionality relies heavily on custom data structures,
so you may also :doc:`check their descriptions <simpletypes>`.

Querying pools
--------------

To query for a list of staking pools, ``Wallet.stake_pools()`` may be used. It accepts the amount
of the stake as optional argument, otherwise it uses wallet's current total balance.

The result is a list of pools, represented by
:class:`StakePoolInfo <cardano.simpletypes.StakePoolInfo>` and sorted by expected long-term
interest, from highest to lowest.

.. code-block:: python

    In [30]: pools = wallet.stake_pools()

    In [31]: pools[0]
    Out[31]: StakePoolInfo(id='pool1tzmx7k40sm8kheam3pr2d4yexrp3jmv8l50suj6crnvn6dc2429', status=<StakePoolStatus.ACTIVE: 1>, ticker=None, name=None, description=None, homepage=None, rewards=StakeRewardMetrics(expected=Decimal('0.182832'), stake=Decimal('1051.689055')), cost=Decimal('340.000000'), margin=Decimal('0.035'), pledge=Decimal('54000000.000000'), relative_stake=Decimal('0.0014'), saturation=Decimal('0.7001171530343129'), produced_blocks=1091, retirement=None)


You may query pools regardless of whether the wallet is currently delegating or not.


Staking status
--------------

The wallet might be in one of two states: delegating or not delegating. However, once delegation
or withdrawal have been scheduled, they would also appear in the list of planned future operations.


Staking
-------

Once decided which stake pool to use, you may delegate the wallet's balance there. The first
argument must be either pool's ID or one of the
:class:`StakePoolInfo <cardano.simpletypes.StakePoolInfo>` objects returned from pool query
described above.

If successful, the result will be the delegation transaction.


Unstaking
---------

Cancelling an ongoing delegation is pretty straightforward. Just use the ``Wallet.unstake()``
method, providing a passphrase and you will get the unstaking transaction as the result.
