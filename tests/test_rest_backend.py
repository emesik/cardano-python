from decimal import Decimal
import json
import responses

from cardano import exceptions
from cardano.address import Address
from cardano.backends.walletrest import WalletREST
from cardano.metadata import Metadata
from cardano.simpletypes import Epoch, StakingStatus
from cardano.transaction import Transaction
from cardano.wallet import WalletService, Wallet

from .base import JSONTestCase


class TestREST(JSONTestCase):
    service = None
    passphrase = "pass.12345678"
    data_subdir = "test_rest_backend"

    def setUp(self):
        super(TestREST, self).setUp()
        self.service = WalletService(WalletREST())

    def _url(self, path):
        return "".join([self.service.backend.base_url, path])

    def test_defaults(self):
        self.assertEqual(self.service.backend.base_url, "http://localhost:8090/v2/")

    @responses.activate
    def test_create_wallet(self):
        responses.add(
            responses.POST,
            self._url("wallets"),
            json=self._read("test_create_wallet-00-POST_wallets.json"),
            status=200,
        )
        wid = self.service.create_wallet(
            name="test wallet",
            mnemonic="resist render west spin antique wild gossip thing syrup network risk gospel seek drop receive",
            passphrase=self.passphrase,
        )
        self.assertIsInstance(wid, str)
        self.assertEqual(wid, "eff9cc89621111677a501493ace8c3f05608c0ce")

    @responses.activate
    def test_retrieve_wallet(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_retrieve_wallet-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(wallet.wid, "eff9cc89621111677a501493ace8c3f05608c0ce")
        self.assertAlmostEqual(wallet.sync_progress(), Decimal(1), places=2)

        status, nexts = wallet.staking_status()
        self.assertIsInstance(status, StakingStatus)
        self.assertFalse(status.delegating)
        self.assertIsNone(status.target_id)
        self.assertIsNone(status.changes_at)
        self.assertEqual(len(nexts), 0)

    @responses.activate
    def test_retrieve_wallet_not_synced(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_retrieve_wallet_not_synced-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(wallet.wid, "eff9cc89621111677a501493ace8c3f05608c0ce")
        self.assertAlmostEqual(wallet.sync_progress(), Decimal("0.9827"), places=4)

        status, nexts = wallet.staking_status()
        self.assertIsInstance(status, StakingStatus)
        self.assertFalse(status.delegating)
        self.assertIsNone(status.target_id)
        self.assertIsNone(status.changes_at)
        self.assertEqual(len(nexts), 0)

    @responses.activate
    def test_retrieve_wallet_with_assets(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_retrieve_wallet_with_assets-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(wallet.wid, "eff9cc89621111677a501493ace8c3f05608c0ce")
        assets = wallet.assets()
        self.assertEqual(len(assets), 1)
        self.assertEqual(
            list(assets.keys())[0],
            ":6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7",
        )
        self.assertEqual(list(assets.values())[0].available, 2)
        self.assertEqual(list(assets.values())[0].total, 2)

    @responses.activate
    def test_list_addresses(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_list_addresses-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_list_addresses-10-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        addresses = wallet.addresses()
        for i, addr in enumerate(addresses):
            self.assertIsInstance(
                addr,
                Address,
                "Address of index {:d} is not an instance of Address but {}".format(
                    i, type(addr)
                ),
            )

    @responses.activate
    def test_list_addresses_with_usage(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_list_addresses_with_usage-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_list_addresses_with_usage-10-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        addresses = wallet.addresses(with_usage=True)
        for i, addr in enumerate(addresses):
            self.assertIsInstance(
                addr[0],
                Address,
                "Address of index {:d} is not an instance of Address but {}".format(
                    i, type(addr)
                ),
            )
            self.assertIsInstance(addr[1], bool)

    @responses.activate
    def test_list_transactions(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_list_transactions-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_list_transactions-10-GET_transactions_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_list_transactions-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        txns = wallet.transactions()
        self.assertEqual(len(txns), 1)
        self.assertIsInstance(txns[0], Transaction)

    @responses.activate
    def test_list_transactions_with_assets(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_list_transactions_with_assets-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_list_transactions_with_assets-10-GET_transactions_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_list_transactions_with_assets-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        txns = wallet.transactions()
        self.assertEqual(len(txns), 4)
        for tx in txns:
            self.assertIsInstance(tx, Transaction)

    @responses.activate
    def test_transfer(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_transfer-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_transfer-10-POST_transfer_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_transfer-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        txn = wallet.transfer(
            "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
            1,
            passphrase=self.passphrase,
        )
        self.assertIsInstance(txn, Transaction)

    @responses.activate
    def test_transfer_multiple(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_transfer_multiple-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_transfer_multiple-10-POST_transfer_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_transfer_multiple-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        txn = wallet.transfer_multiple(
            (
                (
                    "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                    Decimal("1.234567"),
                ),
                (
                    "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                    Decimal("2.345678"),
                ),
            ),
            passphrase=self.passphrase,
        )
        self.assertIsInstance(txn, Transaction)
        self.assertEqual(len(txn.inputs), 1)
        self.assertEqual(len(txn.outputs), 4)
        self.assertEqual(len(txn.local_inputs), 1)
        self.assertEqual(len(txn.local_outputs), 3)
        self.assertEqual(txn.amount_in, Decimal("0"))
        self.assertEqual(txn.amount_out, Decimal("1.234567"))

    @responses.activate
    def test_transfer_with_metadata(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_transfer_with_metadata-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_transfer_with_metadata-10-POST_transfer_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_transfer_with_metadata-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        data = json.loads(
            """
        {
            "10504143639544897702": {
                "int": -1.4304053759886015514e19
            },
            "17329656595257689515": {
                "string": "yQNttsok3EQ"
            },
            "15345559452353729335": {
                "bytes": "fa1212030dd02612eccb"
            },
            "593828266493176337": {
                "list": [
                    {
                        "string": "HaYsLNx7"
                    },
                    {
                        "int": -1.537136810304170744e19
                    }
                ]
            },
            "17200655244803120463": {
                "map": [
                    {
                        "k": {
                            "string": "zNXD7qk"
                        },
                        "v": {
                            "list": []
                        }
                    }
                ]
            }
        }
        """,
            parse_float=Decimal,
        )
        txn = wallet.transfer(
            "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
            1,
            passphrase=self.passphrase,
            metadata=Metadata.deserialize(data),
        )
        self.assertIsInstance(txn, Transaction)
        self.assertIsInstance(txn.metadata, Metadata)
        self.assertDictEqual(txn.metadata, Metadata.deserialize(data))

    @responses.activate
    def test_estimate_fee(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_estimate_fee-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/payment-fees"),
            json=self._read(
                "test_estimate_fee-10-POST_estimate_fee_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/payment-fees"),
            json=self._read(
                "test_estimate_fee-20-POST_estimate_fee_with_metadata_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        est_min, est_max = wallet.estimate_fee(
            (
                (
                    "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                    Decimal("1.234567"),
                ),
                (
                    "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                    Decimal("2.345678"),
                ),
            )
        )
        self.assertEqual(est_min, Decimal("0.174785"))
        self.assertEqual(est_max, Decimal("0.180989"))
        data = json.loads(
            """
        {
            "10504143639544897702": {
                "int": -1.4304053759886015514e19
            },
            "17329656595257689515": {
                "string": "yQNttsok3EQ"
            },
            "15345559452353729335": {
                "bytes": "fa1212030dd02612eccb"
            },
            "593828266493176337": {
                "list": [
                    {
                        "string": "HaYsLNx7"
                    },
                    {
                        "int": -1.537136810304170744e19
                    }
                ]
            },
            "17200655244803120463": {
                "map": [
                    {
                        "k": {
                            "string": "zNXD7qk"
                        },
                        "v": {
                            "list": []
                        }
                    }
                ]
            }
        }
        """,
            parse_float=Decimal,
        )
        metadata = Metadata.deserialize(data)
        est_min, est_max = wallet.estimate_fee(
            (
                (
                    "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                    Decimal("1.234567"),
                ),
                (
                    "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                    Decimal("2.345678"),
                ),
            ),
            metadata=metadata,
        )
        self.assertEqual(est_min, Decimal("0.180989"))
        self.assertEqual(est_max, Decimal("0.187193"))

    @responses.activate
    def test_stake_pools(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_stake_pools-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("stake-pools?stake=1054211650"),
            json=self._read(
                "test_stake_pools-10-GET_stake_pools_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        pools = wallet.stake_pools()
        self.assertEqual(len(pools), 11)
        self.assertEqual(pools[0].rewards.expected, Decimal("0.193229"))
        self.assertEqual(pools[0].rewards.stake, Decimal("1054.211650"))

    @responses.activate
    def test_stake(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_stake-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.PUT,
            self._url(
                "stake-pools/pool1xqh4kl5gzn4av7uf32lxas5k8tsfgvhy3hlnrg0fdp98q42jswr/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"
            ),
            json=self._read(
                "test_stake-10-PUT_stake_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_stake-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        tx = wallet.stake(
            "pool1xqh4kl5gzn4av7uf32lxas5k8tsfgvhy3hlnrg0fdp98q42jswr",
            passphrase=self.passphrase,
        )
        self.assertIsInstance(tx, Transaction)
        self.assertEqual(tx.amount_in, 0)
        self.assertEqual(tx.amount_out, 2)
        self.assertEqual(len(tx.local_inputs), 1)
        self.assertEqual(len(tx.local_outputs), 1)

    @responses.activate
    def test_retrieve_wallet_pre_stake(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_retrieve_wallet_pre_stake-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        status, nexts = wallet.staking_status()
        self.assertIsInstance(status, StakingStatus)
        self.assertFalse(status.delegating)
        self.assertIsNone(status.target_id)
        self.assertIsNone(status.changes_at)
        self.assertEqual(len(nexts), 1)
        nxt = nexts[0]
        self.assertIsInstance(nxt, StakingStatus)
        self.assertTrue(nxt.delegating)
        self.assertIsNotNone(nxt.target_id)
        self.assertIsInstance(nxt.changes_at, Epoch)
        self.assertEqual(nxt.changes_at.number, 130)

    @responses.activate
    def test_unstake(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake-10-DELETE_stake_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_unstake-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        tx = wallet.unstake(passphrase=self.passphrase)
        self.assertIsInstance(tx, Transaction)
        self.assertEqual(tx.amount_in, Decimal("1.827679"))
        self.assertEqual(tx.amount_out, 0)
        self.assertEqual(len(tx.local_inputs), 1)
        self.assertEqual(len(tx.local_outputs), 1)

    @responses.activate
    def test_retrieve_wallet_pre_cancelled_stake(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_retrieve_wallet_pre_cancelled_stake-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        status, nexts = wallet.staking_status()
        self.assertIsInstance(status, StakingStatus)
        self.assertFalse(status.delegating)
        self.assertIsNone(status.target_id)
        self.assertIsNone(status.changes_at)
        # the upcoming delegation has been cancelled but there's still a trace in next list
        self.assertEqual(len(nexts), 1)
        nxt = nexts[0]
        self.assertIsInstance(nxt, StakingStatus)
        self.assertFalse(nxt.delegating)
        self.assertIsNone(nxt.target_id)
        self.assertIsInstance(nxt.changes_at, Epoch)
        self.assertEqual(nxt.changes_at.number, 130)

    @responses.activate
    def test_cancel_ongoing_stake_without_withdrawal(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_cancel_ongoing_stake_without_withdrawal-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_cancel_ongoing_stake_without_withdrawal-10-DELETE_stake-pools_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=403,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        status, nexts = wallet.staking_status()
        self.assertIsInstance(status, StakingStatus)
        self.assertTrue(status.delegating)
        self.assertEqual(
            status.target_id, "pool1tzmx7k40sm8kheam3pr2d4yexrp3jmv8l50suj6crnvn6dc2429"
        )
        self.assertIsNone(status.changes_at)
        with self.assertRaises(exceptions.NonNullRewards):
            wallet.unstake(passphrase=self.passphrase)

    @responses.activate
    def test_withdrawal(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_withdrawal-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.POST,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/transactions"),
            json=self._read(
                "test_withdrawal-10-POST_transfer_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_withdrawal-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        status, nexts = wallet.staking_status()
        self.assertTrue(status.delegating)
        tx = wallet.transfer(
            "addr_test1qpjqfw0xn8wp3rt9633ja6ua2nfmpx70qdn67cutc93p02hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqvy6c2z",
            1,
            allow_withdrawal=True,
            passphrase=self.passphrase,
        )
        self.assertEqual(len(tx.withdrawals), 1)
        self.assertEqual(len(tx.local_outputs), 2)

    @responses.activate
    def test_cancel_ongoing_stake(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_cancel_ongoing_stake-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_cancel_ongoing_stake-10-DELETE_stake-pools_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=202,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_cancel_ongoing_stake-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_cancel_ongoing_stake-30-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        status, nexts = wallet.staking_status()
        self.assertTrue(status.delegating)
        self.assertEqual(wallet.balance().reward, 0)
        tx = wallet.unstake(passphrase=self.passphrase)
        self.assertIsInstance(tx, Transaction)
        status, nexts = wallet.staking_status()
        self.assertTrue(status.delegating)
        self.assertEqual(len(nexts), 1)
        self.assertFalse(nexts[0].delegating)
