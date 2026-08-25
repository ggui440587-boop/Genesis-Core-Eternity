import time
import datetime
import os
import subprocess
from git_auto_sync import GitAutoSync
from scraper_module import ProjectScraperModule
from ai_analyzer_module import AIAnalyzerModule
from logger_alert_module import SystemLogger

# ==============================================================
# Genesis Master Engine - 多語言完全終極整合總大腦
# ==============================================================

class GenesisMasterEngine:
    def __init__(self):
        self.logger = SystemLogger()
        self.logger.log_info("Genesis Master Engine 全端多語言生態系啟動中...")
        self.scraper = ProjectScraperModule()
        self.analyzer = AIAnalyzerModule()

    def run_pipeline(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.log_info(f"觸發完整自動化管線，當前時間: {timestamp}")

        # 0. 執行底層 Shell 系統維護腳本
        try:
            if os.path.exists("system_maintenance.sh"):
                subprocess.run(["./system_maintenance.sh"], check=True)
                self.logger.log_info("步驟 0 (Shell 系統維護) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"Shell 腳本執行異常: {e}")

        # 1. 執行 Node.js 網路非同步模組
        try:
            if os.path.exists("net_worker.js"):
                subprocess.run(["node", "net_worker.js"], check=True)
                self.logger.log_info("步驟 1 (Node.js 網路模組) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"Node.js 模組執行異常: {e}")

        # 2. 執行 C/C++ 高效能運算模組
        try:
            if os.path.exists("./optimizer"):
                subprocess.run(["./optimizer"], check=True)
                self.logger.log_info("步驟 2 (C/C++ 高效能運算模組) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"C 模組執行異常: {e}")

        # 3. 執行 Python 爬蟲與資料庫儲存
        try:
            self.scraper.fetch_and_store(
                title=f"Ultimate Multi-Lang Record - {timestamp}",
                url="https://github.com/ggui440587-boop/Genesis-Core-Eternity"
            )
            self.logger.log_info("步驟 3 (Python 資料抓取與儲存) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"爬蟲模組發生異常: {e}")

        # 4. 執行 Python AI 智慧分析與摘要
        try:
            self.analyzer.analyze_latest_records()
            self.logger.log_info("步驟 4 (AI 智慧分析) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"AI 分析模組發生異常: {e}")

        # 5. 執行 Git 自動同步與遠端備份
        try:
            GitAutoSync.sync_repository()
            self.logger.log_info("步驟 5 (Git 自動同步) 執行成功。")
        except Exception as e:
            self.logger.log_error(f"Git 同步過程發生異常: {e}")

    def start_service(self, interval_seconds=3600):
        self.logger.log_info(f"啟動常駐背景服務，循環間隔: {interval_seconds} 秒")
        try:
            while True:
                self.run_pipeline()
                self.logger.log_info("進入休眠，等待下一次排程觸發...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            self.logger.log_info("收到手動終止訊號，系統安全關閉。")

if __name__ == "__main__":
    engine = GenesisMasterEngine()
    # 測試執行一次完整串聯管線
    engine.run_pipeline()

