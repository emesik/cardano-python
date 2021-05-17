import collections
import enum


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


Epoch = collections.namedtuple("Epoch", ["number", "starts"])


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


StakePoolStatus = enum.Enum("StakePoolStatus", "ACTIVE RETIRING DELISTED")
StakePoolStatus.__doc__ = "Represents stake pool status"

StakeRewardMetrics = collections.namedtuple(
    "StakeRewardMetrics",
    [
        "expected",
        "stake",
    ],
)
StakeRewardMetrics.__doc__ = "Represents stake pool reward metrics"
StakeRewardMetrics.expected.__doc__ = "Expected rewards at the end of an epoch, in ADA"
StakeRewardMetrics.stake.__doc__ = (
    "Staked amount against which rewards were calculated, in ADA"
)

StakePoolInfo = collections.namedtuple(
    "StakePoolInfo",
    [
        "id",
        "status",
        "ticker",
        "name",
        "description",
        "homepage",
        "rewards",
        "cost",
        "margin",
        "pledge",
        "relative_stake",
        "saturation",
        "produced_blocks",
        "retirement",
    ],
)
StakePoolInfo.__doc__ = "Stores stake pool data"
StakePoolInfo.id.__doc__ = "Unique ID"
StakePoolInfo.status.__doc__ = "Status, one of :class:`StakePoolStatus` enum"
StakePoolInfo.ticker.__doc__ = "3-5 chars long ticker"
StakePoolInfo.name.__doc__ = "Name"
StakePoolInfo.description.__doc__ = "Description"
StakePoolInfo.homepage.__doc__ = "Homepage URL"
StakePoolInfo.cost.__doc__ = "Fixed pool running cost in ADA"
StakePoolInfo.margin.__doc__ = "Operator's margin on the total reward before splitting it among stakeholders (as :class:`Decimal` fraction)"
StakePoolInfo.pledge.__doc__ = "Minimal stake amount that the pool is willing to honor"
StakePoolInfo.relative_stake.__doc__ = "The live pool stake relative to the total stake"
StakePoolInfo.saturation.__doc__ = (
    "Saturation-level of the pool based on the desired number "
    "of pools aimed by the network. A value above 1 indicates that the pool is saturated."
)
StakePoolInfo.produced_blocks.__doc__ = (
    "Number of blocks produced by a given stake pool in its lifetime."
)
StakePoolInfo.retirement.__doc__ = "The :class:`Epoch` in which the pool retires"

StakingStatus = collections.namedtuple(
    "StakingStatus",
    [
        "delegating",
        "target_id",
        "changes_at",
    ],
)
StakingStatus.__doc__ = "Wallet's staking status"
StakingStatus.delegating.__doc__ = "Whether the wallet is actively delegating"
StakingStatus.target_id.__doc__ = "The ID of the pool the wallet is delegating to"
StakingStatus.changes_at.__doc__ = ":class:`Epoch` since which the change comes live"
