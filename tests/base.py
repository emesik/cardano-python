import json
import os
import unittest

class JSONTestCase(unittest.TestCase):
    data_subdir = None

    def _read(self, *args):
        path = os.path.join(os.path.dirname(__file__), 'data')
        if self.data_subdir:
            path = os.path.join(path, self.data_subdir)
        path = os.path.join(path, *args)
        with open(path, 'r') as fh:
            return json.loads(fh.read())
