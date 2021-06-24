from ... import exceptions


class WalletRESTException(exceptions.BackendException, exceptions.WalletException):
    def __init__(self, *args, **kwargs):
        self.result = kwargs.pop("result", None)
        super(WalletRESTException, self).__init__(*args, **kwargs)


class BadRequest(WalletRESTException):
    """Raised when the underlying REST API returns HTTP code 400."""

    pass


class NotFound(WalletRESTException):
    """Raised when the underlying REST API returns HTTP code 404."""

    pass


class RESTServerError(WalletRESTException):
    """
    Raised when the underlying REST API returns HTTP code 403 or 500 and the error cannot be
    handled.
    """

    pass


class CreatedInvalidTransaction(WalletRESTException, exceptions.TransactionException):
    pass
