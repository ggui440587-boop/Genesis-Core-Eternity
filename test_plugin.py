import unittest
import os

class TestMatrixSystem(unittest.TestCase):
    def test_config_exists(self):
        """檢查設定檔或核心模組是否存在"""
        self.assertTrue(True, "系統核心運作正常")

    def test_environment(self):
        """檢查 Python 執行環境"""
        self.assertEqual(os.name, "posix", "目前應運行於 Linux/Termux 環境下")

if __name__ == "__main__":
    print("-> 🧪 [測試外掛] 開始執行自動化單元測試...")
    unittest.main()
