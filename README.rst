Python Cardano module
=====================

**This software is in development phase. Please consider it experimental and don't rely on any
API to be stable before version 1.0 comes.**

There's release 0.7 available. It is usable but more advanced features haven't been well tested
yet.

Prerequisites
-------------

1. You need to have a `cardano-node` running.
2. You need to have a `cardano-wallet` running and connected to the node.
3. The rest you find in the `documentation`_.

Please note it is most safe to run both node and wallet software on your local machine. The network
security is well beyond the scope of this documentation, though. Also, I strongly recommend using
the Cardano *testnet* for any software development and testing.

.. _`documentation`: http://cardano-python.readthedocs.io/en/latest/

Roadmap
-------

This module is the implementation of `the idea`_ submitted to Catalyst Project.

.. _`the idea`: https://cardano.ideascale.com/a/dtd/Python-module/333770-48088

+------------+---------+--------------------------------------------------------------------------+
| date       | version | features                                                                 |
+============+=========+==========================================================================+
| 2021-03-16 | 0.1     | - classes for Wallet, Address and Transaction                            |
|            |         | - create wallet from seed                                                |
|            |         | - retrieve wallet                                                        |
|            |         | - check balance                                                          |
|            |         | - list historical transactions                                           |
|            |         | - send transfer                                                          |
+------------+---------+--------------------------------------------------------------------------+
| 2021-03-28 | 0.2     | - fixed transaction API                                                  |
|            |         | - listing native assets (other than ADA)                                 |
|            |         | - docs for 0.1 features                                                  |
+------------+---------+--------------------------------------------------------------------------+
| 2021-04-11 | 0.3     | - add metadata to transactions                                           |
|            |         | - docs for 0.2 features                                                  |
+------------+---------+--------------------------------------------------------------------------+
| 2021-04-18 | 0.4     | - fee estimation                                                         |
+------------+---------+--------------------------------------------------------------------------+
| 2021-04-25 | 0.5     | - stake                                                                  |
|            |         | - unstake                                                                |
|            |         | - docs for 0.4 features                                                  |
+------------+---------+--------------------------------------------------------------------------+
| 2021-05-17 | 0.6     | - UTXO stats                                                             |
|            |         | - docs for 0.5 + 0.6 features                                            |
+------------+---------+--------------------------------------------------------------------------+
| 2021-08-08 | 0.7     | - advanced filtering of incoming and outgoing transfers                  |
|            |         | - native assets transfer                                                 |
+------------+---------+--------------------------------------------------------------------------+
|            |         | **End of the Catalyst-funded phase**                                     |
+------------+---------+--------------------------------------------------------------------------+
| future     |         | - address validation                                                     |
|            |         | - key operations (HD wallet key generation)                              |
|            |         | - seed to key and vice versa conversion                                  |
|            |         | - coin selection                                                         |
|            |         | - transaction forgetting                                                 |
|            |         | - handling of Byron wallets                                              |
|            |         | - Goguen features (smart contracts?)                                     |
+------------+---------+--------------------------------------------------------------------------+


**Q:** Why the roadmap above differs so much from the plan presented in Catalyst proposal?

**A:** While developing the module I discovered that some of the features I had originally declared
were impossible to implement given the available tools. Also, the proposal lacked some features
that are important but somehow I missed them when proposing. The roadmap consists of items I found
both important and doable.

Donate
------

If you like to support the idea with a donation, the address is::

    addr1qy5xfmuxy22h9c82h2fc96du769cyqptn45h9xhqkjwuh07y42xxcwu506y3czyjp00f66r9t2u5nrrunyu867f2fcmskzkcmp

.. image:: donate.qr.png

Thank you.
