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


class AssetID(object):
    """
    Represents the ID of a native Cardano asset. It consists of asset name and policy ID.
    It renders as string representation of ``policy_id:asset_name``.
    """

    asset_name = None
    policy_id = None

    def __init__(self, asset_name, policy_id):
        self.asset_name = asset_name if asset_name is not None else self.asset_name
        self.policy_id = policy_id or self.policy_id

    def __repr__(self):
        return "{:s}:{:s}".format(self.asset_name, self.policy_id)

    def __eq__(self, other):
        if isinstance(other, AssetID):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance(other, bytes):
            return str(self).encode() == other
        return super(AssetID, self).__eq__(other)

    def __hash__(self):
        return hash(str(self))
