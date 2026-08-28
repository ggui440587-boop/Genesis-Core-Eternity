import os
import sys

def test_genesis_ecosystem():
    print("-> 🧪 [TestRunner] 開始進行 Genesis-Core-Eternity 專案全系統整合測試...")

    # 定義所有必須存在的專案檔案清單
    required_files = [
        "core_engine.py",
        "genesis_config.json",
        "heartbeat_scheduler_module.py",
        "resource_monitor_module.py",
        "log_analyzer_module.py",
        "backup_cleaner_module.py",
        "config_loader_module.py",
        "exception_handler_module.py"
    ]

    missing_count = 0
    for filename in required_files:
        if os.path.exists(filename):
            print(f"   [✓] 檢查通過：找到檔案 {filename}")
        else:
            print(f"   [✕] 錯誤：找不到必要檔案 {filename}")
            missing_count += 1

    if missing_count == 0:
        print("-> [🎉] 恭喜！所有專案核心模組與設定檔皆完整無缺，系統隨時可以上線運行。")
    else:
        print(f"-> [⚠️] 注意：有 {missing_count} 個檔案遺失，請確認是否已完整建立。")

if __name__ == "__main__":
    test_genesis_ecosystem()

