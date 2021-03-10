import json
import logging
import operator
import requests

from ...wallet import Balance
from ...numbers import from_lovelaces
from . import exceptions

_log = logging.getLogger(__name__)


class WalletREST(object):
    base_url = None
    timeout = 10

    def __init__(self, protocol="http", host="localhost", port=8090):
        self.base_url = "{protocol}://{host}:{port}/v2/".format(
            protocol=protocol, host=host, port=port
        )
        _log.debug("WalletREST backend url: {:s}".format(self.base_url))

    def raw_request(self, method, path, params=None):
        url = "".join([self.base_url, path])
        hdr = {"Content-Type": "application/json"}
        params = params or {}
        _log.debug(
            u"{method} {url}\nParams:\n{params}".format(
                method=method,
                url=url,
                params=json.dumps(params, indent=2, sort_keys=True),
            )
        )
        rsp = getattr(requests, method.lower())(
            url, headers=hdr, data=json.dumps(params), timeout=self.timeout
        )
        if rsp.status_code != 204:  # if content exists
            result = rsp.json()
            _ppresult = json.dumps(result, indent=2, sort_keys=True)
            _log.debug(u"Result:\n{result}".format(result=_ppresult))
        else:
            result = None
            _log.debug(u"No result (HTTP 204)")
        if rsp.status_code == 404:
            raise exceptions.NotFound(result)
        return result

    def wallet_ids(self):
        return map(operator.itemgetter("id"), self.raw_request("GET", "wallets"))

    def wallet_exists(self, wid):
        try:
            self.raw_request("GET", "wallets/{:s}".format(wid))
        except exceptions.NotFound:
            return False
        return True

    def create_wallet(self, name, mnemonic, passphrase, mnemonic_2f=None):
        data = {
            "name": name,
            "mnemonic_sentence": mnemonic.split(),
            "passphrase": passphrase,
            "address_pool_gap": 20,
        }
        if mnemonic_2f:
            data["mnemonic_second_factor"] = mnemonic_2f.split()
        wdata = self.raw_request("POST", "wallets", data)
        return wdata["id"]

    def delete_wallet(self, wid):
        try:
            self.raw_request("DELETE", "wallets/{:s}".format(wid))
        except exceptions.NotFound:
            return False
        return True

    def balance(self, wid):
        bdata = self.raw_request("GET", "wallets/{:s}".format(wid))["balance"]
        return Balance(
            from_lovelaces(bdata["total"]["quantity"]),
            from_lovelaces(bdata["available"]["quantity"]),
            from_lovelaces(bdata["reward"]["quantity"]),
        )

    def asset_balances(self, wid):
        data = self.raw_request("GET", "wallets/{:s}".format(wid))
        try:
            bdata = data["assets"]
        except KeyError:
            raise exceptions.NotSupported("Extra assets are not supported")
        assets = {}
        for ast in bdata["total"]:
            pid = ast["policy_id"]
            assets[pid] = assets[pid] if pid in assets else {}
            assets[pid]["total"] = ast["quantity"]
        for ast in bdata["available"]:
            pid = ast["policy_id"]
            assets[pid] = assets[pid] if pid in assets else {}
            assets[pid]["available"] = ast["quantity"]
        return {
            pid: Balance(bal["total"], bal["available"], None) for pid, bal in assets
        }

    def addresses(self, wid):
        adata = self.raw_request("GET", "wallets/{:s}/addresses".format(wid))
        return map(operator.itemgetter("id"), adata)
