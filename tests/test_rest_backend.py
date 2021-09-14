from decimal import Decimal
import json
import responses

from cardano import exceptions
from cardano.address import Address
from cardano.backends.walletrest import WalletREST
from cardano.metadata import Metadata
from cardano.simpletypes import Epoch, StakingStatus, AssetID
from cardano.transaction import Transaction
from cardano.wallet import WalletService, Wallet

from .base import JSONTestCase


class TestSinglewallet(JSONTestCase):
    service = None
    passphrase = "pass.12345678"
    data_subdir = "test_rest_backend"

    def setUp(self):
        super(TestSinglewallet, self).setUp()
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
        self.assertEqual(len(assets), 14)
        exp_assets = {
            AssetID("6c6f766164616e6674", "0c306361512844fbdb83294f278937c04af6e56ab1d94d2dd187d725"),
            AssetID("6c6f766164616e6674", "0f5e9e9143f4eb0317584aa295d0d2dc9741edfdbbe1af64f241aa32"),
            AssetID("6c6f766164616e6674", "19b5961ad59574e2eb90d80894bbca8b51b7e2fbfe8ac649697c1255"),
            AssetID("6c6f766164616e6674", "1c088dec595714fb23d3eb806dcffaaaec8c275b502e2cc047026012"),
            AssetID("6c6f766164616e6674", "2efcadf7209b422c7742c1b1ceb8b82cfd6ae6b099226bc195daddfa"),
            AssetID("6c6f766164616e6674", "57fbec4da0c525282f50f2ff2567ecb529c276ea972dd31a1e1d8e41"),
            AssetID("6c6f766164616e6674", "618e9db244d4832faf1bd937a423f3f8aea558bed396f74fa82f8fea"),
            AssetID("6c6f766164616e6674", "6604684337b45547a5fdfb418c6ad140aba3d02e65b0bb0dc3c492a1"),
            AssetID("6c6f766164616e6674", "68bf925a392af499964003a5caaef10edd1ceac7d2c08e7bd7b287d0"),
            AssetID("6c6f766164616e6674", "73d4f77b57be5bbdf7c7cb475662083a4111f6e018cffb056142f14e"),
            AssetID("6c6f766164616e6674", "88c5393b19640c59611a73bf7ec7e7884fc228544a24b2e384d3ed32"),
            AssetID("6c6f766164616e6674", "9dfc0ed69a98a12f97b6a74e6a41cfb9aecdc5883b2ecbf2f9d13672"),
            AssetID("6c6f766164616e6674", "b03f3f89862ecb51522832535e525ec014c884e047f63acc786567bb"),
            AssetID("6c6f766164616e6674", "dcb9bccdb63474aaa16f0ef041c59c582bbd85ad19cca7119ba5ea79"),
        }
        self.assertSetEqual(set(assets.keys()), exp_assets)
        for asset_id, balance in assets.items():
            self.assertEqual(balance.available, balance.total)
            self.assertGreater(balance.total, 0)
            self.assertIsNone(balance.reward)

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
    def test_unstake_before_start(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_before_start-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_before_start-10-DELETE_stake_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_unstake_before_start-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
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
    def test_unstake_without_withdrawal(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_without_withdrawal-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_without_withdrawal-10-DELETE_stake-pools_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
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
    def test_unstake_after_withdrawal(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_after_withdrawal-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.DELETE,
            self._url("stake-pools/*/wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_after_withdrawal-10-DELETE_stake-pools_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=202,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_unstake_after_withdrawal-20-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_unstake_after_withdrawal-30-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
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

    @responses.activate
    def test_utxo_stats(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce"),
            json=self._read(
                "test_utxo_stats-00-GET_wallets_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url(
                "wallets/eff9cc89621111677a501493ace8c3f05608c0ce/statistics/utxos"
            ),
            json=self._read(
                "test_utxo_stats-10-GET_utxo_stats_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        total, dist, scale = wallet.utxo_stats()
        self.assertEqual(total, Decimal("1052.422864"))
        self.assertIsInstance(dist, dict)
        self.assertEqual(len(dist), 17)
        self.assertEqual(scale, "log10")


class TestDoublewallet(JSONTestCase):
    service = None
    wida = "04aebef49c24086f603db7a6d157f915c5c9411a"
    widb = "5e27c10c9cb253c93a771732fd7dcbb56d34bc47"
    passphrasea = "pass.12345678"
    passphraseb = "pass.87654321"
    data_subdir = "test_rest_backend"

    @responses.activate
    def setUp(self):
        self.service = WalletService(WalletREST())
        responses.add(
            responses.GET,
            self._url("wallets/{:s}".format(self.wida)),
            json=self._read(
                "test_transfer_asset-30-GET_wallets_{:s}.json".format(self.wida)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}".format(self.widb)),
            json=self._read(
                "test_transfer_asset-60-GET_wallets_{:s}.json".format(self.widb)
            ),
            status=200,
        )
        super(TestDoublewallet, self).setUp()
        self.wala = self.service.wallet(
            self.wida, passphrase=self.passphrasea
        )
        self.walb = self.service.wallet(
            self.widb, passphrase=self.passphraseb
        )

    def _url(self, path):
        return "".join([self.service.backend.base_url, path])

    @responses.activate
    def test_transfer_asset(self):
        responses.add(
            responses.POST,
            self._url("wallets/{:s}/transactions".format(self.wala.wid)),
            json=self._read(
                "test_transfer_asset-10-POST_transfer_{:s}.json".format(self.wala.wid)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}/addresses".format(self.wala.wid)),
            json=self._read(
                "test_transfer_asset-20-GET_addresses_{:s}.json".format(self.wala.wid)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}".format(self.wala.wid)),
            json=self._read(
                "test_transfer_asset-30-GET_wallets_{:s}.json".format(self.wala.wid)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}/transactions".format(self.walb.wid)),
            json=self._read(
                "test_transfer_asset-40-GET_transactions_{:s}.json".format(self.walb.wid)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}/addresses".format(self.walb.wid)),
            json=self._read(
                "test_transfer_asset-50-GET_addresses_{:s}.json".format(self.walb.wid)
            ),
            status=200,
        )
        responses.add(
            responses.GET,
            self._url("wallets/{:s}".format(self.walb.wid)),
            json=self._read(
                "test_transfer_asset-60-GET_wallets_{:s}.json".format(self.walb.wid)
            ),
            status=200,
        )

        asset_id = AssetID(
            "", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        tx_out = self.wala.transfer(
            "addr_test1qqpwa4lv202c9q4fag5kepr0jjnreq8yxrjgau7u4ulppa9c69u4ed55s8p7nuef3z65fkjjxcslwdu3h75zl7zeuzgqv3l7cc",
            2,
            assets=[(asset_id, 1)],
        )
        self.assertEqual(tx_out.amount_in, 0)
        self.assertEqual(tx_out.amount_out, 2)
        self.assertEqual(len(tx_out.inputs), 2)         # one with asset, one with fee
        self.assertEqual(len(tx_out.local_inputs), 2)   # both are local
        self.assertEqual(len(tx_out.outputs), 2)        # payment + change
        self.assertEqual(len(tx_out.local_outputs), 1)  # change

        assetsa = self.wala.assets()
        self.assertEqual(len(assetsa), 1)
        self.assertIn(asset_id, assetsa)
        self.assertEqual(assetsa[asset_id].total, 1)
        self.assertEqual(assetsa[asset_id].available, 1)

        tx_in = self.walb.transactions()[0]
        self.assertEqual(tx_in.amount_in, 2)
        self.assertEqual(tx_in.amount_out, 0)
        self.assertEqual(len(tx_in.inputs), 2)          # one with asset, one with fee
        self.assertEqual(len(tx_in.local_inputs), 0)    # none are local
        self.assertEqual(len(tx_in.outputs), 2)         # payment + change
        self.assertEqual(len(tx_in.local_outputs), 1)   # payment

        assetsb = self.walb.assets()
