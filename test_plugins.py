import unittest
from heartbeat_plugin import HeartbeatPlugin
from crypto_plugin import CryptoPlugin

class TestMatrixPlugins(unittest.TestCase):
    def test_heartbeat(self):
        hb = HeartbeatPlugin()
        beat = hb.pulse()
        self.assertGreaterEqual(beat, 1)

    def test_crypto(self):
        crypto = CryptoPlugin()
        encoded = crypto.encrypt_data("TestCode")
        decoded = crypto.decrypt_data(encoded)
        self.assertEqual(decoded, "TestCode")

if __name__ == "__main__":
    unittest.main()
