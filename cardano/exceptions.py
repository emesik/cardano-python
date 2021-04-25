class CardanoException(Exception):
    pass


class BackendException(CardanoException):
    pass


class WalletException(CardanoException):
    pass


class MissingPassphrase(WalletException):
    pass


class TransactionException(WalletException):
    pass


class PoolAlreadyJoined(WalletException):
    pass
