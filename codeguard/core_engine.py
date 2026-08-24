import time
import datetime
import os
from git_auto_sync import GitAutoSync
from scraper_module import ProjectScraperModule

# ==============================================================
# Genesis Master Engine - 整合大腦中控、爬蟲與自動同步
# ==============================================================

class GenesisMasterEngine:
    def __init__(self):
        print("=" * 60)
        print(" 🌟 [Genesis Master Engine] 系統全面啟動中...")
        print("=" * 60)
        self.scraper = ProjectScraperModule()
        self.check_environment()

    def check_environment(self):
        print("-> 🔍 檢查工作目錄與必要模組...")
        if os.path.exists("git_auto_sync.py") and os.path.exists("scraper_module.py"):
            print("   [✓] 所有核心模組載入正常")
        else:
            print("   [!] 警告: 部分模組缺失")

    def run_pipeline(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-> ⏱️ 觸發完整管線 (Pipeline)，當前時間: {timestamp}")

        # 1. 執行資料抓取與儲存模組 (由爬蟲模組寫入 SQLite)
        print("-> 🕷️ 執行資料抓取與本地資料庫儲存...")
        try:
            self.scraper.fetch_and_store(
                title=f"Automated Sync Record - {timestamp}",
                url="https://github.com/ggui440587-boop/Genesis-Core-Eternity"
            )
            print("   [✓] 資料寫入資料庫完成。")
        except Exception as e:
            print(f"   [✕] 資料寫入異常: {e}")

        # 2. 串聯自動同步模組，將最新資料與程式碼推送到 GitHub
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
    engine = GenesisMasterEngine()
    # 測試執行一次完整管線，或直接啟動常駐服務
    engine.run_pipeline()

