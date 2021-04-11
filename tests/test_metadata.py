from decimal import Decimal
import json
import unittest

from cardano.metadata import Metadata


class MetadataValidationTestCase(unittest.TestCase):
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


class MetadataSerDeserTestCase(unittest.TestCase):
    def test_serialize_simple(self):
        data = {
            1943: "bike trip",
            1986: 426,
            1: bytes([0xAC, 0xAB]),
            2: bytearray([0xFE, 0xED, 0xBA, 0xDB, 0xEE, 0xF0]),
        }
        m = Metadata(data.items())
        d = m.serialize()
        self.assertEqual(len(d), 4)
        self.assertIn("1", d)
        self.assertIn("2", d)
        self.assertIn("1943", d)
        self.assertIn("1986", d)
        self.assertDictEqual(d["1"], {"bytes": "acab"})
        self.assertDictEqual(d["2"], {"bytes": "feedbadbeef0"})
        self.assertDictEqual(d["1943"], {"string": "bike trip"})
        self.assertDictEqual(d["1986"], {"int": 426})

    def test_serialize_deserialize_simple(self):
        data = {
            1943: "bike trip",
            1986: 426,
            1: bytes([0xAC, 0xAB]),
            2: bytearray([0xFE, 0xED, 0xBA, 0xDB, 0xEE, 0xF0]),
        }
        m = Metadata(data.items())
        m2 = Metadata.deserialize(m.serialize())
        self.assertDictEqual(data, m2)

    def test_serialize_list(self):
        data = {
            997: [
                "an example",
                321,
                "of multitype".encode("ascii"),
                ["nested", "list", 0],
            ]
        }
        m = Metadata(data.items())
        d = m.serialize()
        self.assertEqual(len(d), 1)

    def test_serialize_deserialize_list(self):
        data = {
            997: [
                "an example",
                321,
                "of multitype".encode("ascii"),
                ["nested", "list", 0],
            ]
        }
        m = Metadata(data.items())
        m2 = Metadata.deserialize(m.serialize())
        self.assertDictEqual(data, m2)
        self.assertEqual(data[997], m2[997])

    def test_deserialize_complex(self):
        """
        Deserializes example taken from
        https://github.com/input-output-hk/cardano-node/blob/master/doc/reference/tx-metadata.md#detailed-schema

        WARNING: The element of the map where the key is another map, has been removed from the
        data. This is because Python doesn't support mutable objects being keys to dicts (in
        particular, a dict cannot be a key). This is a TODO issue #5.
        """
        txdata = json.loads(
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
        m = Metadata.deserialize(txdata)
        self.assertEqual(len(m), 5)
        self.assertIsInstance(m[10504143639544897702], int)
        self.assertEqual(m[10504143639544897702], -14304053759886015514)
        self.assertIsInstance(m[17329656595257689515], str)
        self.assertEqual(m[17329656595257689515], "yQNttsok3EQ")
        self.assertIsInstance(m[15345559452353729335], bytes)
        self.assertEqual(
            m[15345559452353729335],
            bytes([0xFA, 0x12, 0x12, 0x03, 0x0D, 0xD0, 0x26, 0x12, 0xEC, 0xCB]),
        )
        self.assertIsInstance(m[593828266493176337], list)
        self.assertIsInstance(m[593828266493176337][0], str)
        self.assertIsInstance(m[593828266493176337][1], int)
        self.assertEqual(m[593828266493176337], ["HaYsLNx7", -15371368103041707440])
        self.assertIsInstance(m[17200655244803120463], dict)
        self.assertDictEqual(m[17200655244803120463], {"zNXD7qk": []})
