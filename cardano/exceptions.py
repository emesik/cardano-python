class CardanoException(Exception):
    """The base exception for cardano-python module."""

    pass


class BackendException(CardanoException):
    """The base exception for backend errors."""

    pass


class WalletException(CardanoException):
    """The base exception for wallet errors."""

    pass


class MissingPassphrase(WalletException):
    """Raised when the wallet is missing a required passphrase."""

    pass


class TransactionException(WalletException):
    """Base for errors with constructing or handling transactions."""

    pass


class CannotCoverFee(TransactionException):
    pass


class StakingException(WalletException):
    """Base error when delegating, withdrawing or cancelling stake."""

    pass


class PoolAlreadyJoined(StakingException):
    """Raised when trying to double-stake."""

    pass


class NonNullRewards(StakingException):
    """Raised when trying to cancel stake without withdrawing rewards first."""

    pass
