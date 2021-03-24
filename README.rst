Python Cardano module
=====================

**This software is in early development phase. Please consider it experimental and don't rely on any
API to be stable in the future.**

There's first release (0.1) available for those brave enough to try it.

This module is the implementation of `the idea`_ submitted to Catalyst Project.

.. _`the idea`: https://cardano.ideascale.com/a/dtd/Python-module/333770-48088

Roadmap
-------

The roadmap is delayed from what I posted originally in the proposal. This is because I've mistaken
the voting dates. Right now the vote is still underway but I've started the work already.

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
| 2021-03-28 | 0.2     | - listing native assets (other than ADA)                                 |
|            |         | - create new payment addresses                                           |
|            |         | - docs for 0.1 features                                                  |
+------------+---------+--------------------------------------------------------------------------+
| 2021-04-06 | 0.3     | - add metadata to transactions                                           |
|            |         | - fee estimation                                                         |
|            |         | - stake                                                                  |
|            |         | - unstake                                                                |
|            |         | - docs for 0.2 features                                                  |
+------------+---------+--------------------------------------------------------------------------+
| 2021-04-19 | 0.4     | - UTXO stats                                                             |
|            |         | - coin selection                                                         |
|            |         | - address validation                                                     |
|            |         | - docs for 0.3 + 0.4 features                                            |
+------------+---------+--------------------------------------------------------------------------+

Also, there are optional features that aren't included in the Catalyst proposal.
I'll try to implement them if time permits, otherwise the list below will become a TODO once
the Catalyst-funded phase concludes.

- key operations (HD wallet key generation)
- seed to key and vice versa conversion
- advanced filtering of incoming and outgoing transfers
- transaction forgetting
- handling of Byron wallets
- Goguen features (smart contracts?)

Donate
------

If you like to support the idea with a donation, the address is::

    addr1qy5xfmuxy22h9c82h2fc96du769cyqptn45h9xhqkjwuh07y42xxcwu506y3czyjp00f66r9t2u5nrrunyu867f2fcmskzkcmp

.. image:: donate.qr.png

Thank you.
