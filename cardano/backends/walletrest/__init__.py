from decimal import Decimal
import json
import logging
import operator
import requests
import urllib

from ... import exceptions as main_exceptions
from ...metadata import Metadata
from ...numbers import from_lovelaces, to_lovelaces
from ...simpletypes import (
    AssetID,
    Balance,
    StakePoolInfo,
    StakePoolStatus,
    StakeRewardMetrics,
    StakingStatus,
)
from ...transaction import Transaction
from . import exceptions
from . import serializers

_log = logging.getLogger(__name__)


class JSONWithDecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(JSONWithDecimalEncoder, self).default(o)


class WalletREST(object):
    base_url = None
    timeout = 10

    ERR2EXCEPTION = {
        403: {
            "pool_already_joined": main_exceptions.PoolAlreadyJoined,
            "non_null_rewards": main_exceptions.NonNullRewards,
        },
        500: {
            "created_invalid_transaction": exceptions.CreatedInvalidTransaction,
        },
    }

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
            result = rsp.json(parse_float=Decimal)
            _ppresult = json.dumps(
                rsp.json(), cls=JSONWithDecimalEncoder, indent=2, sort_keys=True
            )
            _log.debug(u"Result:\n{result}".format(result=_ppresult))
        else:
            result = None
            _log.debug(u"No result (HTTP 204)")
        if rsp.status_code == 400:
            raise exceptions.BadRequest(result["message"], result=result)
        if rsp.status_code == 403:
            try:
                raise self.ERR2EXCEPTION[rsp.status_code][result["code"]](
                    result["message"]
                )
            except KeyError:
                pass
            raise exceptions.RESTServerError(result.get("message", "* NO MESSAGE *"))
        if rsp.status_code == 404:
            raise exceptions.NotFound(result["message"], result=result)
        if rsp.status_code == 500:
            try:
                raise self.ERR2EXCEPTION[rsp.status_code][result["code"]](
                    result["message"], result=result
                )
            except KeyError:
                pass
            raise exceptions.RESTServerError(
                result.get("message", "* NO MESSAGE *"), result=result
            )
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

    def sync_progress(self, wid):
        wdata = self.raw_request("GET", "wallets/{:s}".format(wid))
        return (
            1.0
            if wdata["state"]["status"] == "ready"
            else wdata["state"]["progress"]["quantity"] / Decimal(100)
        )

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
            aid = AssetID(ast["asset_name"], ast["policy_id"])
            assets[aid] = assets[aid] if aid in assets else {}
            assets[aid]["total"] = ast["quantity"]
        for ast in bdata["available"]:
            aid = AssetID(ast["asset_name"], ast["policy_id"])
            assets[aid] = assets[aid] if aid in assets else {}
            assets[aid]["available"] = ast["quantity"]
        return {
            aid: Balance(bal["total"], bal["available"], None)
            for aid, bal in assets.items()
        }

    def addresses(self, wid):
        adata = self.raw_request("GET", "wallets/{:s}/addresses".format(wid))
        return [(ad["id"], True if ad["state"] == "used" else False) for ad in adata]

    def _addresses_set(self, wid):
        return set(map(operator.itemgetter(0), self.addresses(wid)))

    def _txdata2tx(self, txd, addresses=None):
        inputs = (
            [serializers.get_input(inp) for inp in txd["inputs"]]
            if "inputs" in txd
            else []
        )
        outputs = (
            [serializers.get_output(outp) for outp in txd["outputs"]]
            if "outputs" in txd
            else []
        )
        local_inputs = set()
        local_outputs = set()
        amount = Decimal(0)
        if addresses:
            for out in outputs:
                if out.address and out.address in addresses:
                    local_outputs.add(out)
                    amount += out.amount
            for inp in inputs:
                if inp.address and inp.address in addresses:
                    local_inputs.add(inp)
        fee = serializers.get_amount(txd["fee"])
        metadata = (
            Metadata.deserialize(txd["metadata"])
            if txd.get("metadata", None) is not None
            else None
        )
        return Transaction(
            txid=txd["id"],
            amount=amount,
            fee=fee,
            inserted_at=serializers.get_block_position(txd["inserted_at"])
            if "inserted_at" in txd
            else None,
            expires_at=serializers.get_block_position(txd["expires_at"])
            if "expires_at" in txd
            else None,
            pending_since=serializers.get_block_position(txd["pending_since"])
            if "pending_since" in txd
            else None,
            inputs=inputs,
            outputs=outputs,
            local_inputs=local_inputs,
            local_outputs=local_outputs,
            withdrawals=[
                (serializers.get_amount(w["amount"]), w["stake_address"])
                for w in txd.get("withdrawals", [])
            ],
            metadata=metadata,
        )

    def transactions(self, wid, start=None, end=None, order="ascending"):
        data = {
            "order": order,
        }
        if start is not None:
            data["start"] = start.isoformat(timespec="seconds")
        if end is not None:
            data["end"] = end.isoformat(timespec="seconds")
        return [
            self._txdata2tx(txd, addresses=self._addresses_set(wid))
            for txd in self.raw_request(
                "GET", "wallets/{:s}/transactions".format(wid), data
            )
        ]

    def transfer(self, wid, destinations, metadata, allow_withdrawal, ttl, passphrase):
        data = {
            "passphrase": passphrase,
            "withdrawal": "self" if allow_withdrawal else None,
            "payments": [
                {
                    "address": str(address),
                    "amount": serializers.store_amount(amount),
                }
                for (address, amount) in destinations
            ],
        }
        if metadata is not None:
            if not isinstance(metadata, Metadata):
                metadata = Metadata(metadata.items())
            data["metadata"] = metadata.serialize()
        if ttl is not None:
            data["time_to_live"] = serializers.store_interval(ttl)
        # NOTE: the order of the following two requests is important
        txd = self.raw_request("POST", "wallets/{:s}/transactions".format(wid), data)
        return self._txdata2tx(txd, addresses=self._addresses_set(wid))

    def estimate_fee(self, wid, destinations, metadata):
        data = {
            "payments": [
                {
                    "address": str(address),
                    "amount": serializers.store_amount(amount),
                }
                for (address, amount) in destinations
            ],
        }
        if metadata is not None:
            if not isinstance(metadata, Metadata):
                metadata = Metadata(metadata.items())
            data["metadata"] = metadata.serialize()
        feedata = self.raw_request(
            "POST", "wallets/{:s}/payment-fees".format(wid), data
        )
        return (
            serializers.get_amount(feedata["estimated_min"]),
            serializers.get_amount(feedata["estimated_max"]),
        )

    def _stakepoolinfo(self, pooldata, stake):
        retirement = (
            serializers.get_epoch(pooldata["retirement"])
            if "retirement" in pooldata and "epoch_number" in pooldata["retirement"]
            else None
        )
        status = (
            StakePoolStatus.DELISTED
            if "flags" in pooldata and "delisted" in pooldata["flags"]
            else StakePoolStatus.RETIRING
            if retirement
            else StakePoolStatus.ACTIVE
        )
        if "metadata" in pooldata:
            ticker = pooldata["metadata"]["ticker"]
            name = pooldata["metadata"]["name"]
            description = pooldata["metadata"]["description"]
            homepage = pooldata["metadata"]["homepage"]
        else:
            ticker = name = description = homepage = None
        rewards = StakeRewardMetrics(
            serializers.get_amount(pooldata["metrics"]["non_myopic_member_rewards"]),
            stake,
        )
        return StakePoolInfo(
            pooldata["id"],
            status,
            ticker,
            name,
            description,
            homepage,
            rewards,
            serializers.get_amount(pooldata["cost"]),
            serializers.get_percent(pooldata["margin"]),
            serializers.get_amount(pooldata["pledge"]),
            serializers.get_percent(pooldata["metrics"]["relative_stake"]),
            pooldata["metrics"]["saturation"],
            pooldata["metrics"]["produced_blocks"]["quantity"],
            retirement,
        )

    def stake_pools(self, wid, stake):
        urldata = {"stake": to_lovelaces(stake)}
        poolsdata = self.raw_request(
            "GET", "?".join(("stake-pools", urllib.parse.urlencode(urldata)))
        )
        return [self._stakepoolinfo(pool, stake) for pool in poolsdata]

    def _stakingstatus(self, data):
        return StakingStatus(
            serializers.get_stakingstatus(data["status"]),
            data["target"] if "target" in data else None,
            serializers.get_epoch(data["changes_at"]) if "changes_at" in data else None,
        )

    def staking_status(self, wid):
        sdata = self.raw_request("GET", "wallets/{:s}".format(wid))["delegation"]
        active = sdata["active"]
        return (
            self._stakingstatus(active),
            [self._stakingstatus(ss) for ss in sdata["next"]],
        )

    def stake(self, wid, pool_id, passphrase):
        txdata = self.raw_request(
            "PUT",
            "stake-pools/{:s}/wallets/{:s}".format(pool_id, wid),
            {"passphrase": passphrase},
        )
        return self._txdata2tx(txdata, addresses=self._addresses_set(wid))

    def unstake(self, wid, passphrase):
        txdata = self.raw_request(
            "DELETE",
            "stake-pools/*/wallets/{:s}".format(wid),
            {"passphrase": passphrase},
        )
        return self._txdata2tx(txdata, addresses=self._addresses_set(wid))

    def utxo_stats(self, wid):
        sdata = self.raw_request(
            "GET",
            "wallets/{:s}/statistics/utxos".format(wid),
            {},
        )
        return (
            serializers.get_amount(sdata["total"]),
            {
                from_lovelaces(int(lvl)): num
                for (lvl, num) in sorted(
                    sdata["distribution"].items(), key=operator.itemgetter(0)
                )
            },
            sdata["scale"],
        )
