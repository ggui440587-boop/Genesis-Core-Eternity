import logging
import os

# ==============================================================
# System Logger & Test Module - 系統日誌記錄與自動化測試模組
# ==============================================================

LOG_FILE = "genesis_system.log"

# 設定日誌格式與輸出檔案
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SystemLogger:
    @staticmethod
    def log_info(message):
        """記錄一般運作訊息"""
        logging.info(message)
        print(f"[日誌記錄] 🟢 {message}")

    @staticmethod
    def log_error(error_message):
        """記錄錯誤與異常訊息"""
        logging.error(error_message)
        print(f"[日誌記錄] 🔴 發現錯誤: {error_message}")

    @staticmethod
    def run_self_test():
        """執行模組自我測試，確保核心檔案存在"""
        SystemLogger.log_info("開始執行生態系模組自我測試...")
        required_files = ["main_ecosystem.py", "genesis_config.json"]

        for file in required_files:
            if os.path.exists(file):
                SystemLogger.log_info(f"檢查通過：找到必要檔案 [{file}]")
            else:
                SystemLogger.log_error(f"檢查失敗：缺少必要檔案 [{file}]")

if __name__ == "__main__":
    print("=" * 60)
    print(" 📋 系統日誌與測試模組啟動")
    print("=" * 60)
    SystemLogger.run_self_test()
    print(f"-> 詳情已寫入日誌檔: {os.path.abspath(LOG_FILE)}")

