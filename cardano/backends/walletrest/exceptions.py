from ... import exceptions


class WalletRESTException(exceptions.BackendException):
    pass


class NotFound(WalletRESTException):
    pass
