.. image:: https://ucarecdn.com/86a7f7fd-8931-4d80-9732-bee6ab78d854/-/format/webp/-/resize/1500/
   :width: 200pt

Python module for Cardano
=========================

Welcome to the documentation for the ``cardano`` Python module.

The aim of this project is to offer a set of tools for interacting with Cardano blockchain platform
in Python. It provides higher level classes representing objects from the Cardano environment, like
wallets, addresses, transactions.

Currently it operates over REST protocol offered by the ``cardano-wallet`` binary, however, a
forward compatibility for implementing other backends is one of the key features.

Project homepage: https://github.com/emesik/cardano-python

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   wallet
   address
   transactions
   nativeassets
   staking
   extras

   simpletypes
   exceptions
   backends.walletrest


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
