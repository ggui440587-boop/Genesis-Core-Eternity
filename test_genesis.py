# -*- coding: utf-8 -*-
import unittest
import genesis_core_eternity as core

class TestGenesisCore(unittest.TestCase):
    def test_core_hook(self):
        self.assertTrue(core.ultimate_async_hook())

if __name__ == '__main__':
    unittest.main()
