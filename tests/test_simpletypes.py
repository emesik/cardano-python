import unittest

from cardano.simpletypes import AssetID

class TestComparisons(unittest.TestCase):
    def test_cmp_same_assetid(self):
        asset1 = AssetID("6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7", "name")
        asset2 = AssetID("6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7", "name")
        self.assertEqual(asset1, asset2)

    def test_cmp_different_name_assetid(self):
        asset1 = AssetID("name1", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        asset2 = AssetID("name2", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        self.assertNotEqual(asset1, asset2)

    def test_cmp_different_id_assetid(self):
        asset1 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        asset2 = AssetID("name", "a1a815a7323c69c86abbafb66dbfdb1aa76b8d07d69639e9413dd637")
        self.assertNotEqual(asset1, asset2)

    def test_cmp_assetid_to_string(self):
        asset1 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        asset2 = "name:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        self.assertEqual(asset1, asset2)

    def test_cmp_string_to_assetid(self):
        asset1 = "name:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7"
        asset2 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        self.assertEqual(asset1, asset2)

    def test_cmp_assetid_to_bytes(self):
        asset1 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        asset2 = "name:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7".encode()
        self.assertEqual(asset1, asset2)

    def test_cmp_bytes_to_assetid(self):
        asset1 = "name:6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7".encode()
        asset2 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        self.assertEqual(asset1, asset2)

    def test_cmp_assetid_to_none(self):
        asset1 = AssetID("name", "6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7")
        self.assertNotEqual(asset1, None)
