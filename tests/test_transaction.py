from decimal import Decimal
import unittest

from cardano.transaction import Transaction


class TransactionArgsTestCase(unittest.TestCase):
    def test_simple(self):
        tx = Transaction(
            txid="0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264"
        )
        self.assertIsNone(tx.gross_amount)
        self.assertIsNone(tx.fee)
        with self.assertRaises(TypeError):
            tx.amount
        self.assertIsInstance(tx.inputs, list)
        self.assertIsInstance(tx.outputs, list)
        self.assertEqual(len(tx.inputs), 0)
        self.assertEqual(len(tx.outputs), 0)

    def test_args(self):
        tx = Transaction(
            txid="88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c",
            gross_amount=Decimal("1.168801"),
            fee=Decimal("0.168801"),
        )
        self.assertIsInstance(tx.amount, Decimal)
        self.assertEqual(tx.amount, Decimal("1"))

    def test_inherited(self):
        class CustomTx(Transaction):
            txid = "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
            gross_amount = Decimal("1.168801")
            fee = Decimal("0.168801")

        tx = CustomTx()
        self.assertEqual(
            tx.txid, "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
        )
        self.assertEqual(tx.gross_amount, Decimal("1.168801"))
        self.assertEqual(tx.fee, Decimal("0.168801"))
        self.assertIsInstance(tx.amount, Decimal)
        self.assertEqual(tx.amount, Decimal("1"))

    def test_inherited_with_args(self):
        class CustomTx(Transaction):
            txid = "0b048162778e29e98d833d948a3be7f18f9ce8693d7ee407c7d38b6ef2a5a264"
            gross_amount = Decimal("1000.000000")
            fee = Decimal("0.000000")

        tx = CustomTx(
            "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c",
            gross_amount=Decimal("1.168801"),
            fee=Decimal("0.168801"),
        )
        self.assertEqual(
            tx.txid, "88633270f854eea5b2f35a863d748b294299deecf62ec9629ff08fca87fff45c"
        )
        self.assertEqual(tx.gross_amount, Decimal("1.168801"))
        self.assertEqual(tx.fee, Decimal("0.168801"))
        self.assertIsInstance(tx.amount, Decimal)
        self.assertEqual(tx.amount, Decimal("1"))
