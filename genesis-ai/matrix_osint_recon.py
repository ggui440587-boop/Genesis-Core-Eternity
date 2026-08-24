import os
import sqlite3
import requests
import datetime

class MatrixOSINTRecon:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[OSINT-Recon] 正在初始化主動威脅與開源情報（OSINT）偵查網...")
        self.init_osint_table()

    def init_osint_table(self):
        """建立 OSINT 專屬情報表"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS osint_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                source_url TEXT,
                severity TEXT,
                discovered_at TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("[🛡️ OSINT] 威脅與情報資料表已就緒。")

    def scan_global_tech_trends(self):
        """模擬或主動抓取全球開源與資安最新趨勢情報"""
        print("[🌐 深度偵查] 正在向全球開源情報節點與技術 API 發起雷達掃描...")
        
        # 這裡我們模擬透過公開 API（如 GitHub Trending 或開源資安公告）擷取最新動向
        # 實際應用中可串接 CVE 資料庫、GitHub Security Advisories 或 Hacker News
        simulated_intel_stream = [
            {
                "title": "Zero-Day Vulnerability Discovered in Popular Linux Kernel Network Stack (CVE-2026-XXXX)",
                "url": "https://github.com/advisories",
                "severity": "HIGH"
            },
            {
                "title": "New High-Performance Local Vector RAG Architecture Released for Edge Devices",
                "url": "https://huggingface.co/blog",
                "severity": "INFO"
            }
        ]

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        new_count = 0
        for item in simulated_intel_stream:
            title = item["title"]
            url = item["url"]
            severity = item["severity"]
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 檢查是否已經收錄過
            cursor.execute("SELECT id FROM osint_vault WHERE title = ?", (title,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO osint_vault (title, source_url, severity, discovered_at) VALUES (?, ?, ?, ?)",
                    (title, url, severity, time_str)
                )
                new_count += 1
                print(f"[🎯 捕獲情報]等級 [{severity}] -> {title}")

        conn.commit()
        conn.close()
        print(f"[✅ OSINT 掃描完畢] 本輪成功截獲並建檔 {new_count} 筆全球開源新情報！")

    def execute_recon_cycle(self):
        self.scan_global_tech_trends()

if __name__ == "__main__":
    recon = MatrixOSINTRecon()
    recon.execute_recon_cycle()

