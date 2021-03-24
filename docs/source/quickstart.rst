Quick start
===========

This quick start tutorial will guide you through the first steps of connecting
to the Cardano wallet software. We assume:

 1. You have installed and started `cardano-node`_. (If there's no package for your OS, you may
    consider installing a Docker image, however many of the tutorials out there are out of date.)
 2. The node has synchronized the blockchain.
 3. You have installed and started `cardano-wallet`_.
 4. The wallet software is connected to the node.
 5. You know how to use CLI (*command line interface*).
 6. You have some experience with Python.

.. _`cardano-node`: https://github.com/input-output-hk/cardano-node
.. _`cardano-wallet`: https://github.com/input-output-hk/cardano-wallet

Use testnet for your own safety
-------------------------------

The testnet is another Cardano network where worthless coins circulate and where, as the name
suggests, all tests are supposed to be run. It's also a place for early deployment of future
features of the platform itself.

.. warning:: **Please run all tests on testnet.** The code presented in these docs will
    perform the requested operations right away, without asking for confirmation.
    This is live code, not a wallet application that makes sure the user has not
    made a mistake. **Running on the mainnet, if you make a mistake, you may lose
    money.**


Connect to the wallet
---------------------

For brevity, the following example assumes thet you have an existing wallet of id
``eff9cc89621111677a501493ace8c3f05608c0ce`` and the ``cardano-wallet`` is listening locally on
port 8090. In the following chapter you'll also learn how to create a new wallet from seed.

.. code-block:: python

    In [1]: from cardano.wallet import Wallet

    In [2]: from cardano.backends.walletrest import WalletREST

    In [3]: wal = Wallet("eff9cc89621111677a501493ace8c3f05608c0ce", backend=WalletREST(port=8090))

    In [4]: wal.sync_progress()
    Out[4]: 1.0

    In [5]: wal.balance()
    Out[5]: Balance(total=Decimal('998.831199'), available=Decimal('998.831199'), reward=Decimal('0.000000'))

Congratulations! You have connected to the wallet. You may now proceed to the
next section, which will tell you about :doc:`interaction with wallet <wallet>`.
