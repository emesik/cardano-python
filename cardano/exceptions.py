class CardanoException(Exception):
    """The base exception for cardano-python module."""

    pass


class BackendException(CardanoException):
    """The base exception for backend errors."""

    pass


class WalletServiceException(CardanoException):
    """The base exception for wallet service errors."""

    pass


class WalletAlreadyExists(WalletServiceException):
    """Raised when a duplicate wallet is requested to be created at the service."""

    pass


class WalletException(CardanoException):
    """The base exception for wallet errors."""

    pass


class MissingPassphrase(WalletException):
    """Raised when the wallet is missing a required passphrase."""

    pass


class WrongPassphrase(WalletException):
    """Raised when the provided passphrase doesn't match the wallet's."""

    pass


class TransactionException(WalletException):
    """Base for errors with constructing or handling transactions."""

    pass


class NotEnoughMoney(TransactionException):
    """Raised when the balance is too low."""

    pass


class CannotCoverFee(TransactionException):
    pass


class UTXOTooSmall(TransactionException):
    """Raised when the resulting UTXO with assets has too small ADA amount."""

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


class AlreadyWithdrawing(StakingException):
    """Raised whan another withdrawal attempt is being made while one is already pending."""

    pass
