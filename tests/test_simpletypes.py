from binascii import hexlify
import unittest

from cardano.simpletypes import AssetID


class TestCodec(unittest.TestCase):
    def test_ascii(self):
        name = "test coin"
        name_hex = hexlify(name.encode("ascii")).decode()
        asset = AssetID(
            name_hex, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertEqual(asset.name_bytes, name.encode("ascii"))

    def test_utf8(self):
        name = "zażółć gęślą jaźń"
        name_hex = hexlify(name.encode("utf-8")).decode()
        asset = AssetID(
            name_hex, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertEqual(asset.name_bytes, name.encode("utf-8"))


class TestComparisons(unittest.TestCase):
    def test_cmp_same_assetid(self):
        name = hexlify("name".encode())
        asset1 = AssetID(
            name,
            "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7",
        )
        asset2 = AssetID(
            name,
            "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7",
        )
        self.assertEqual(asset1, asset2)

    def test_cmp_different_name_assetid(self):
        name1 = hexlify("name1".encode())
        name2 = hexlify("name2".encode())
        asset1 = AssetID(
            name1, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        asset2 = AssetID(
            name2, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertNotEqual(asset1, asset2)

    def test_cmp_different_id_assetid(self):
        name = hexlify("name".encode())
        asset1 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        asset2 = AssetID(
            name, "a1a815a7323c69c86abbafb66dbfdb1aa76b8d07d69639e9413dd637"
        )
        self.assertNotEqual(asset1, asset2)

    def test_cmp_assetid_to_string(self):
        name = hexlify("name".encode())
        asset1 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        asset2 = "6e616d65:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        self.assertEqual(asset1, asset2)

    def test_cmp_string_to_assetid(self):
        name = hexlify("name".encode())
        asset1 = "6e616d65:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        asset2 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertEqual(asset1, asset2)

    def test_cmp_assetid_to_bytes(self):
        name = hexlify("name".encode())
        asset1 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        asset2 = (
            "6e616d65:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7".encode()
        )
        self.assertEqual(asset1, asset2)

    def test_cmp_bytes_to_assetid(self):
        name = hexlify("name".encode())
        asset1 = (
            "6e616d65:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7".encode()
        )
        asset2 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertEqual(asset1, asset2)

    def test_cmp_assetid_to_none(self):
        name = hexlify("name".encode())
        asset1 = AssetID(
            name, "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        )
        self.assertNotEqual(asset1, None)
