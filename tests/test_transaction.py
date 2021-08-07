from decimal import Decimal
import operator
import unittest

from cardano.simpletypes import BlockPosition
from cardano.transaction import Transaction, Input, Output, TxFilter


class TransactionArgsTestCase(unittest.TestCase):
    def test_simple(self):
        tx = Transaction(
            txid="0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264"
        )
        self.assertEqual(tx.amount_in, 0)
        self.assertEqual(tx.amount_out, 0)
        self.assertIsNone(tx.fee)
        self.assertIsInstance(tx.inputs, list)
        self.assertIsInstance(tx.outputs, list)
        self.assertEqual(len(tx.inputs), 0)
        self.assertEqual(len(tx.outputs), 0)

    def test_args(self):
        inp = Input("f9ab4d2dbb270370172d28cb280c2351771998ab4405fb90fb93bb18aee216fa")
        tx = Transaction(
            txid="88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c",
            fee=Decimal("0.168801"),
            inputs=[inp],
        )
        self.assertEqual(len(tx.inputs), 1)
        self.assertEqual(len(tx.local_inputs), 0)
        self.assertIsInstance(tx.amount_in, Decimal)
        self.assertEqual(tx.amount_in, Decimal("0"))
        self.assertIsInstance(tx.amount_out, Decimal)
        self.assertEqual(tx.amount_out, Decimal("0"))

    def test_inherited(self):
        class CustomTx(Transaction):
            txid = "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
            fee = Decimal("0.168801")

        tx = CustomTx()
        self.assertEqual(
            tx.txid, "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
        )
        self.assertEqual(tx.fee, Decimal("0.168801"))
        self.assertIsInstance(tx.amount_in, Decimal)
        self.assertEqual(tx.amount_in, Decimal("0"))
        self.assertIsInstance(tx.amount_out, Decimal)
        self.assertEqual(tx.amount_out, Decimal("0"))

    def test_inherited_with_args(self):
        class CustomTx(Transaction):
            txid = "0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264"
            fee = Decimal("0.000000")

        tx = CustomTx(
            "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c",
            fee=Decimal("0.168801"),
        )
        self.assertEqual(
            tx.txid, "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
        )
        self.assertEqual(tx.fee, Decimal("0.168801"))
        self.assertIsInstance(tx.amount_in, Decimal)
        self.assertEqual(tx.amount_in, Decimal("0"))
        self.assertIsInstance(tx.amount_out, Decimal)
        self.assertEqual(tx.amount_out, Decimal("0"))


class TransactionIOTestCase(unittest.TestCase):
    def test_amount_calculation_outgoing(self):
        inputs = (
            Input(
                "0000000000000000000000000000000000000000000000000000000000000000",
                "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                Decimal(100),
            ),
        )
        outputs = (
            # this is a change output
            Output(
                "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                Decimal(30),
            ),
            # this is a real outgoing output
            Output(
                "addr_test1qpyppguxp7vlr77eywsvx9f9l0w07fkx7echm0wldaud9ucxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flkns8556zj",
                Decimal(69),
            ),
        )
        tx = Transaction(
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            fee=Decimal(1),
            inputs=inputs,
            outputs=outputs,
            local_inputs=inputs,
            local_outputs=(outputs[0],),
        )
        self.assertEqual(tx.amount_in, 0)
        self.assertEqual(tx.amount_out, 69)

    def test_amount_calculation_incoming(self):
        inputs = (
            Input(
                "0000000000000000000000000000000000000000000000000000000000000000",
                "addr_test1qqr585tvlc7ylnqvz8pyqwauzrdu0mxag3m7q56grgmgu7sxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flknswgndm3",
                Decimal(100),
            ),
        )
        outputs = (
            # this is a real incoming output
            Output(
                "addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e",
                Decimal(30),
            ),
            # this is a change output
            Output(
                "addr_test1qpyppguxp7vlr77eywsvx9f9l0w07fkx7echm0wldaud9ucxu2hyfhlkwuxupa9d5085eunq2qywy7hvmvej456flkns8556zj",
                Decimal(69),
            ),
        )
        tx = Transaction(
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            fee=Decimal(1),
            inputs=inputs,
            outputs=outputs,
            local_inputs=(),
            local_outputs=(outputs[0],),
        )
        self.assertEqual(tx.amount_in, 30)
        self.assertEqual(tx.amount_out, 0)


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.txset = [
            Transaction(
                txid="1f2f3c0bb8bffe6b01c7dd15255b9d125e1e72c630c4f13f2d96e055c364349b",
                inserted_at=BlockPosition(
                    epoch=123, slot=140937, absolute_slot=22907337, height=2458048
                ),
                status="in_ledger",
            ),
            # the following two share the same block
            Transaction(
                txid="747787b69580e56649963d2bbedc067e57265ef385b0546bc38c8bc565ed00fa",
                inserted_at=BlockPosition(
                    epoch=122, slot=262150, absolute_slot=22596550, height=2447816
                ),
                status="in_ledger",
            ),
            Transaction(
                txid="b5876751c9cec196db1d98c2e9335b94ef5974ece7b57f2afed337f9be7ceaad",
                inserted_at=BlockPosition(
                    epoch=122, slot=262150, absolute_slot=22596550, height=2447816
                ),
                status="in_ledger",
            ),
            # this one is just a block later
            Transaction(
                txid="ad39ce00981de18919933d39576f80c0cbc1f5b20ef9e1ecbaa454873d8b6828",
                inserted_at=BlockPosition(
                    epoch=122, slot=262151, absolute_slot=24478170, height=2447817
                ),
                status="in_ledger",
            ),
            Transaction(
                txid="c352a31f22d7b3265284501274535cf0de3a9d59ab47ce16cf851057dbb0b090",
                inserted_at=BlockPosition(
                    epoch=131, slot=8876, absolute_slot=25010210, height=2487126
                ),
                status="in_ledger",
            ),
            # mempool
            Transaction(
                txid="7000bceff12b142009d6967259bddfb93afea9c3d1bfac7cc3a0306785c24ee8",
                status="pending",
            ),
            Transaction(
                txid="52e9167c6292f74b08c9a6e8e9c1f68220ad1d08a404b6f906c51e67bea4699c",
                status="pending",
            ),
        ]

    def test_order(self):
        filtered = TxFilter(unconfirmed=True).filter(self.txset)
        abslots = [
            (tx.inserted_at.absolute_slot if tx.inserted_at is not None else None)
            for tx in filtered
        ]
        self.assertEqual(
            abslots,
            [
                None,
                None,
                25010210,
                24478170,
                22907337,
                22596550,
                22596550,
            ],
        )

    def test_zeros(self):
        filter_min = TxFilter(min_epoch=0, min_slot=0, min_absolute_slot=0)
        filter_max = TxFilter(
            max_epoch=Decimal("inf"),
            max_slot=Decimal("inf"),
            max_absolute_slot=Decimal("inf"),
        )
        by_min = filter_min.filter(self.txset)
        self.assertEqual(len(by_min), 5)
        by_max = filter_max.filter(self.txset)
        self.assertEqual(len(by_max), 5)

    def test_txid(self):
        filtered = TxFilter(
            txid="ad39ce00981de18919933d39576f80c0cbc1f5b20ef9e1ecbaa454873d8b6828"
        ).filter(self.txset)
        self.assertEqual(len(filtered), 1)

    def test_txids(self):
        filtered = TxFilter(
            txid=[
                "ad39ce00981de18919933d39576f80c0cbc1f5b20ef9e1ecbaa454873d8b6828",
                "1f2f3c0bb8bffe6b01c7dd15255b9d125e1e72c630c4f13f2d96e055c364349b",
            ]
        ).filter(self.txset)
        self.assertEqual(len(filtered), 2)

    def test_epoch_range_min(self):
        filtered = TxFilter(min_epoch=131).filter(self.txset)
        self.assertEqual(len(filtered), 1)

    def test_epoch_range_max(self):
        filtered = TxFilter(max_epoch=130).filter(self.txset)
        self.assertEqual(len(filtered), 4)

    def test_epoch_range_both(self):
        filtered = TxFilter(max_epoch=130, min_epoch=123).filter(self.txset)
        self.assertEqual(len(filtered), 1)

    def test_height_range_min(self):
        filtered = TxFilter(
            min_height=2450000,
        ).filter(self.txset)
        self.assertEqual(len(filtered), 2)

    def test_height_range_max(self):
        filtered = TxFilter(max_height=2447816).filter(self.txset)
        self.assertEqual(len(filtered), 2)

    def test_height_range_both(self):
        filtered = TxFilter(max_height=2450000, min_height=2447817).filter(self.txset)
        self.assertEqual(len(filtered), 1)

    def test_slot_range_min(self):
        filtered = TxFilter(
            min_slot=200000,
        ).filter(self.txset)
        self.assertEqual(len(filtered), 3)

    def test_slot_range_max(self):
        filtered = TxFilter(max_slot=262150).filter(self.txset)
        self.assertEqual(len(filtered), 4)

    def test_slot_range_both(self):
        filtered = TxFilter(max_slot=10000, min_slot=8000).filter(self.txset)
        self.assertEqual(len(filtered), 1)

    def test_absolute_slot_range_min(self):
        filtered = TxFilter(
            min_absolute_slot=22907000,
        ).filter(self.txset)
        self.assertEqual(len(filtered), 3)

    def test_absolute_slot_range_max(self):
        filtered = TxFilter(max_absolute_slot=23000000).filter(self.txset)
        self.assertEqual(len(filtered), 3)

    def test_absolute_slot_range_both(self):
        filtered = TxFilter(
            max_absolute_slot=23000000, min_absolute_slot=22907000
        ).filter(self.txset)
        self.assertEqual(len(filtered), 1)
