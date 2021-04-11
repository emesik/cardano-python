from decimal import Decimal
import json
import responses

from cardano.address import Address
from cardano.backends.walletrest import WalletREST
from cardano.metadata import Metadata
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
    def test_used_addresses(self):
        responses.add(
            responses.GET,
            self._url("wallets/eff9cc89621111677a501493ace8c3f05608c0ce/addresses"),
            json=self._read(
                "test_used_addresses-00-GET_addresses_eff9cc89621111677a501493ace8c3f05608c0ce.json"
            ),
            status=200,
        )
        used_addresses = self.service.backend.used_addresses(
            "eff9cc89621111677a501493ace8c3f05608c0ce"
        )
        self.assertIsInstance(used_addresses, set)
        self.assertEqual(len(used_addresses), 2)
        self.assertIn(
            "addr_test1qr9ujxmsvdya6r4e9lxlu4n37svn52us7z8uzqdkhw8muqld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqzuzvzt",
            used_addresses,
        )
        self.assertIn(
            "addr_test1qp64xq7fsz9kvjwjy5tzfpetp2jmmhhk68kw066wqvyfgvhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqj7msh0",
            used_addresses,
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
