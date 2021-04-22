from decimal import Decimal
import unittest

from cardano.transaction import Transaction, Input, Output


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
