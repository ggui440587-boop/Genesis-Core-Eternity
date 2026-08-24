import time
import datetime
import os
from git_auto_sync import GitAutoSync
from scraper_module import ProjectScraperModule
from ai_analyzer_module import AIAnalyzerModule

# ==============================================================
# Genesis Master Engine - 完整生態系統整核心
# ==============================================================

class GenesisMasterEngine:
    def __init__(self):
        print("=" * 60)
        print(" 🌟 [Genesis Master Engine] 完整生態系啟動中...")
        print("=" * 60)
        self.scraper = ProjectScraperModule()
        self.analyzer = AIAnalyzerModule()

    def run_pipeline(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-> ⏱️ 觸發完整自動化管線，當前時間: {timestamp}")
        
        # 1. 執行爬蟲與資料庫儲存
        print("-> 🕷️ [步驟 1] 執行資料抓取與本地資料庫儲存...")
        try:
            self.scraper.fetch_and_store(
                title=f"Ecosystem Sync Record - {timestamp}",
                url="https://github.com/ggui440587-boop/Genesis-Core-Eternity"
            )
        except Exception as e:
            print(f"   [✕] 爬蟲模組異常: {e}")

        # 2. 執行 AI 智慧分析與摘要
        print("-> 🧠 [步驟 2] 執行 AI 智慧分析模組...")
        try:
            self.analyzer.analyze_latest_records()
        except Exception as e:
            print(f"   [✕] AI 分析模組異常: {e}")

        # 3. 執行 Git 自動同步與遠端備份
        print("-> 🚀 [步驟 3] 啟動 Git 自動同步與備份流程...")
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
    # 測試執行一次完整串聯管線
    engine.run_pipeline()

