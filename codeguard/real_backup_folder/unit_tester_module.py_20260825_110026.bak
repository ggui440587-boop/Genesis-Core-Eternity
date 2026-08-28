import unittest
import os

class GenesisSystemTester(unittest.TestCase):
    def test_core_files_exist(self):
        """檢查核心必要檔案是否存在"""
        self.assertTrue(os.path.exists("core_engine.py"), "找不到 core_engine.py 核心檔案")
        self.assertTrue(os.path.exists("system_maintenance.sh"), "找不到 system_maintenance.sh 腳本")

    def test_log_file_creatable(self):
        """檢查系統日誌是否能正常寫入"""
        log_path = "genesis_system.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("TEST_LOG_ENTRY\n")
        self.assertTrue(os.path.exists(log_path), "系統日誌寫入失敗")

if __name__ == "__main__":
    print("-> 🧪 [UnitTester] 開始執行 Genesis 系統自動化單元測試...")
    unittest.main()

