from ... import exceptions


class WalletRESTException(exceptions.BackendException):
    def __init__(self, *args, **kwargs):
        self.result = kwargs.pop("result", None)
        super(WalletRESTException, self).__init__(*args, **kwargs)


class BadRequest(WalletRESTException):
    pass


class NotFound(WalletRESTException):
    pass


class RESTServerError(WalletRESTException):
    pass


class CreatedInvalidTransaction(WalletRESTException, exceptions.TransactionException):
    pass
