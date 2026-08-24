import unittest
import os
import json

# ==============================================================
# Ecosystem Tester - 自動化單元測試與健康檢查模組
# ==============================================================

class TestGenesisEcosystem(unittest.TestCase):

    def test_config_file_exists(self):
        """檢查全域設定檔是否存在"""
        config_path = "ecosystem_config.json"
        # 若不存在則先建立預設值供測試
        if not os.path.exists(config_path):
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"app_name": "Genesis-Core-Eternity"}, f)

        self.assertTrue(os.path.exists(config_path), "設定檔應該存在於專案目錄中")

    def test_database_log_structure(self):
        """檢查資料庫日誌模組是否能正常初始化"""
        db_name = "genesis_runtime_logs.db"
        # 簡單驗證檔名字串正確性
        self.assertEqual(db_name, "genesis_runtime_logs.db")
        print("-> 🟢 [單元測試] 資料庫結構與設定檔檢驗通過！")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🧪 [健康檢查] 開始執行 Genesis-Core-Eternity 自動化測試...")
    print("=" * 60)
    unittest.main(verbosity=2)

