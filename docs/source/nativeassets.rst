Working with native assets
==========================

With Mary era Cardano introduced native assets to the network. Unlike other popular platforms,
Cardano doesn't need smart contracts to handle them. The assets are indivisible (amounts are
integers) and their handling is somewhat different than of ADA.

Asset IDs
---------

Since different native assets may bear the same name, the actual identifier of an asset consists of
``asset_name`` and ``policy_id``. They are grouped together into
:class:`cardano.simpletypes.AssetID`, a class which supports equality operator.

Balances
--------

The wallet has ``.assets()`` method which returns a dict where keys are
:class:`cardano.simpletypes.AssetID` and values are :class:`cardano.simpletypes.Balance` objects.
At the moment the balances have always ``None`` as reward and total equal to available but that
may perhaps change in the future.

.. code-block:: python

    In [9]: wal.assets()
    Out[9]: {6c6f766164616e6674:0c306361512844fbdb83294f278937c04af6e56ab1d94d2dd187d725: Balance(total=1, available=1, reward=None), 6c6f766164616e6674:0f5e9e9143f4eb0317584aa295d0d2dc9741edfdbbe1af64f241aa32: Balance(total=1, available=1, reward=None)}

Sending assets
--------------

Transfer of assets can be specified by additional keyword to the ``Wallet.transfer()`` function or
third element of ``destinations`` item passed to ``Wallet.transfer_multiple()``. An example of
sending 2.0 ADA along with a single native token is:

.. code-block:: python

    In [10]: wal.transfer(
            "addr_test1qqpwa4lv202c9q4fag5kepr0jjnreq8yxrjgau7u4ulppa9c69u4ed55s8p7nuef3z65fkjjxcslwdu3h75zl7zeuzgqv3l7cc",
            2,
            assets=[
                (
                    AssetID(
                        "7461786174696f6e206973207468656674",
                        "6b8d07d69639e9413aa637a1a815a7123c69c86abbafb66dbfdb1aa7"
                        ),
                    1)
            ])

