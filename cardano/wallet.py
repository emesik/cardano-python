import collections

from .address import address


class WalletService(object):
    def __init__(self, backend=None):
        self.backend = backend

    def wallets(self):
        return [Wallet(self.backend, wid) for wid in self.backend.wallet_ids()]

    def wallet(self, wid):
        return Wallet(self.backend, wid)

    def create_wallet(self, name, mnemonic, passphrase, mnemonic_2f=None):
        """
        Creates/restores a wallet. Returns only ID as the backend may need some time to sync
        before being able to return full wallet data.
        """
        return self.backend.create_wallet(name, mnemonic, passphrase, mnemonic_2f)


Balance = collections.namedtuple("Balance", ["total", "available", "reward"])


class Wallet(object):
    def __init__(self, backend, wid):
        self.backend = backend
        self.wid = wid
        if not self.backend.wallet_exists(wid):
            raise ValueError("Wallet of id '{:s}' doesn't exist.".format(wid))

    def addresses(self):
        return [address(addr, wallet=self) for addr in self.backend.addresses(self.wid)]

    def balance(self):
        return self.backend.balance(self.wid)

    def assets(self):
        return self.backend.asset_balances(self.wid)

    def delete(self):
        return self.backend.delete_wallet(self.wid)
