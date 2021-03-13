import responses

from cardano.wallet import WalletService, Wallet
from cardano.backends.walletrest import WalletREST
from cardano.transaction import Transaction

from .base import JSONTestCase


class TestREST(JSONTestCase):
    service = None
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
            passphrase="pass.12345678",
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
        self.assertAlmostEqual(wallet.sync_progress(), 1.0, places=2)

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
        self.assertAlmostEqual(wallet.sync_progress(), 0.9827, places=4)

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
        wallet = self.service.wallet("eff9cc89621111677a501493ace8c3f05608c0ce")
        txns = wallet.transactions()
        self.assertEqual(len(txns), 1)
        self.assertIsInstance(txns[0], Transaction)
