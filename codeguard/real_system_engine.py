import os
import sys
import platform
import sqlite3
from datetime import datetime

class RealSystemEngine:
    def __init__(self, db_path="real_production.db"):
        self.db_path = db_path
        self.init_real_database()

    def init_real_database(self):
        """在本地實體儲存空間建立真實的 SQLite 資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform_info TEXT,
                cpu_count INTEGER,
                execution_time TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print(f"-> [真實存在] 已成功在本地路徑建立真實資料庫檔案: {self.db_path}")

    def collect_and_save_real_data(self):
        """收集真實的系統硬體數據並寫入資料庫與實體檔案"""
        plat = platform.platform()
        cores = os.cpu_count() or 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 寫入真實資料庫
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO real_system_logs (platform_info, cpu_count, execution_time) VALUES (?, ?, ?)",
            (plat, cores, now)
        )
        conn.commit()
        conn.close()

        # 同時寫入實體文字記錄檔
        with open("real_execution_report.log", "a", encoding="utf-8") as f:
            f.write(f"[{now}] 平台: {plat} | 可用核心數: {cores}\n")

        print(f"-> [執行成功]真實數據已寫入資料庫與 real_execution_report.log 檔案！")

if __name__ == "__main__":
    engine = RealSystemEngine()
    engine.collect_and_save_real_data()

