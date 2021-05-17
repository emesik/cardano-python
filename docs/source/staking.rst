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

The wallet might be in one of two states: delegating or not delegating. Additionally, once delegation
or withdrawal have been scheduled, they would also appear in the list of planned future operations.

.. code-block:: python

    In [32]: wallet.staking_status()
    Out[32]: (StakingStatus(delegating=True, target_id='pool1tzmx7k40sm8kheam3pr2d4yexrp3jmv8l50suj6crnvn6dc2429', changes_at=None), [])


The second element of the tuple returned by ``Wallet.staking_status()`` is a list of scheduled
future staking status changes.

Staking
-------

Once decided which stake pool to use, you may delegate the wallet's balance there. The first
argument must be either pool's ID or one of the
:class:`StakePoolInfo <cardano.simpletypes.StakePoolInfo>` objects returned from pool query
described above.

If successful, the result will be the delegation transaction.

.. code-block:: python

    In [33]: tx = wallet.stake("pool1xqh4kl5gzn4av7uf32lxas5k8tsfgvhy3hlnrg0fdp98q42jswr")

    In [34]: tx.amount_out
    Out[34]: Decimal('2.000000')


Unstaking
---------

Cancelling an ongoing delegation is pretty straightforward. Just use the ``Wallet.unstake()``
method, providing a passphrase and you will get the unstaking transaction as the result.

However, if you have a positive reward balance in the wallet, it needs to be withdrawn first. You
may do it by calling the ``Wallet.transfer()`` method for an amount higher than the accumulated
reward and directing it to your first unused local address, for example:

.. code-block:: python

    In [33]: wallet.balance()
    Out[33]: Balance(total=Decimal('1050.770234'), available=Decimal('1050.520254'), reward=Decimal('0.249980'))

    In [34]: wtx = wallet.transfer(wallet.first_unused_address(), Decimal(1), allow_withdrawal=True)

    In [35]: wtx.withdrawals
    Out[35]: [(Decimal('0.249980'), 'stake_test1urk6dxxc3qp9mk7hvjpm95acm6vp2evjm6fdg8542s3jg8qtsgmvf')]

    In [36]: utx = wallet.unstake()

    In [37]: wallet.staking_status()
    Out[37]: (StakingStatus(delegating=True, target_id='pool1tzmx7k40sm8kheam3pr2d4yexrp3jmv8l50suj6crnvn6dc2429', changes_at=None), [StakingStatus(delegating=False, target_id=None, changes_at=Epoch(number=134, starts=datetime.datetime(2021, 5, 24, 20, 20, 16, tzinfo=tzutc())))])
