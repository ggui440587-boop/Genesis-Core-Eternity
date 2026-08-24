import time
import datetime
import os
from git_auto_sync import GitAutoSync

# ==============================================================
# Genesis Core Eternity - 完整串聯主控核心
# ==============================================================

class GenesisMasterEngine:
    def __init__(self):
        print("=" * 60)
        print(" 🌟 [Genesis Master Engine] 系統全面啟動中...")
        print("=" * 60)
        self.check_environment()

    def check_environment(self):
        print("-> 🔍 檢查工作目錄與必要模組...")
        if os.path.exists("git_auto_sync.py"):
            print("   [✓] 發現 Git 自動同步模組")
        else:
            print("   [!] 警告: 未找到 git_auto_sync.py")

    def run_pipeline(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-> ⏱️ 觸發完整管線 (Pipeline)，當前時間: {timestamp}")

        # 1. 執行核心業務與資料處理模組
        print("-> ⚙️ 執行核心資料處理與運算...")
        # (未來可在此處加入你的爬蟲、資料庫或 AI 運算邏輯)

        # 2. 串聯自動同步模組，將成果推送到 GitHub
        print("-> 🚀 啟動自動同步與備份流程...")
        try:
            GitAutoSync.sync_repository()
            print("   [✓] 遠端同步流程執行完畢。")
        except Exception as e:
            print(f"   [✕] 同步過程發生異常: {e}")

    def start_service(self, interval_seconds=3600):
        print(f"-> 🔄 啟動常駐背景服務，循環間隔: {interval_seconds} 秒")
        try:
            while True:
                self.run_pipeline()
                print(f"-> 💤 進入休眠，等待下一次排程觸發...\n" + "-"*50)
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n-> 🛑 收到手動終止訊號，系統安全關閉。")

if __name__ == "__main__":
    # 初始化並執行主引擎（預設每 1 小時執行一次完整串聯循環）
    engine = GenesisMasterEngine()
    engine.start_service(interval_seconds=3600)

