import collections


Balance = collections.namedtuple("Balance", ["total", "available", "reward"])
Balance.__doc__ = "Represents a balance of asset, including total, principal and reward"
Balance.total.__doc__ = "The total balance"
Balance.available.__doc__ = "The principal, i.e. the total minus staking rewards"
Balance.reward.__doc__ = "The staking rewards (interest)"


BlockPosition = collections.namedtuple(
    "BlockPosition", ["epoch", "slot", "absolute_slot"]
)
BlockPosition.__doc__ = "Represents block's position within the blockchain"
BlockPosition.epoch.__doc__ = "Epoch number"
BlockPosition.slot.__doc__ = "Slot number"
BlockPosition.absolute_slot.__doc__ = "Absolute slot number"
