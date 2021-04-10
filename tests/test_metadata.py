import unittest

from cardano.metadata import Metadata


class MetadataTestCase(unittest.TestCase):
    def test_valid_keys(self):
        m = Metadata([(1, "abc")])
        self.assertIn(1, m)
        self.assertEqual(m[1], "abc")
        m[4] = "foo"
        self.assertIn(4, m)
        self.assertEqual(m[4], "foo")

    def test_invalid_keys(self):
        m = Metadata()
        with self.assertRaises(KeyError):
            m["a"] = "a"
        with self.assertRaises(KeyError):
            m[b"a"] = "a"
        with self.assertRaises(KeyError):
            m[-1] = "a"
        with self.assertRaises(KeyError):
            m[2 ** 64] = "a"

    def test_valid_values(self):
        m = Metadata()
        m[1] = "foo"
        m[2] = 234
        m[3] = ["foo", "bar", "baz"]
        m[4] = {1: "foo", "bar": "baz"}

    def test_invalid_int_value(self):
        m = Metadata()
        with self.assertRaises(ValueError):
            m[1] = -(2 ** 64) - 2
        with self.assertRaises(ValueError):
            m[1] = 2 ** 64
        with self.assertRaises(ValueError):
            Metadata([(1, -(2 ** 64) - 2)])
        with self.assertRaises(ValueError):
            Metadata([(1, 2 ** 64)])

    def test_invalid_string_value(self):
        m = Metadata()
        with self.assertRaises(ValueError):
            m[1] = "12345678901234567890123456789012345678901234567890123456789012345"
        with self.assertRaises(ValueError):
            m[
                1
            ] = "12345678901234567890123456789012345678901234567890123456789012345".encode(
                "ascii"
            )
        with self.assertRaises(ValueError):
            m[1] = bytearray(
                "12345678901234567890123456789012345678901234567890123456789012345".encode(
                    "ascii"
                )
            )
        with self.assertRaises(ValueError):
            Metadata(
                [
                    (
                        1,
                        "12345678901234567890123456789012345678901234567890123456789012345",
                    )
                ]
            )
        with self.assertRaises(ValueError):
            Metadata(
                [
                    (
                        1,
                        "12345678901234567890123456789012345678901234567890123456789012345".encode(
                            "ascii"
                        ),
                    )
                ]
            )
        with self.assertRaises(ValueError):
            Metadata(
                [
                    (
                        1,
                        bytearray(
                            "12345678901234567890123456789012345678901234567890123456789012345".encode(
                                "ascii"
                            )
                        ),
                    )
                ]
            )

    def test_invalid_list_value(self):
        m = Metadata()
        with self.assertRaises(ValueError):
            m[1] = [1, "abc"]
        with self.assertRaises(ValueError):
            Metadata([(1, [1, "abc"])])

    def test_invalid_mapping_value(self):
        m = Metadata()
        with self.assertRaises(ValueError):
            m[1] = {2 ** 64: "abc"}
        with self.assertRaises(ValueError):
            Metadata([(1, {2 ** 64: "abc"})])

    def test_invalid_value_type(self):
        m = Metadata()
        with self.assertRaises(TypeError):
            m[1] = None
        with self.assertRaises(TypeError):
            Metadata([(1, None)])
