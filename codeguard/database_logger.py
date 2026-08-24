import sqlite3
import datetime
import os

# ==============================================================
# Database Logger Module - 本地資料庫持久化與運行日誌模組
# ==============================================================

class DatabaseLogger:
    DB_NAME = "genesis_runtime_logs.db"

    @classmethod
    def init_database(cls):
        """初始化並建立執行日誌資料庫與資料表"""
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS runtime_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_level TEXT,
                message TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def log_event(cls, level, message):
        """將系統運行事件寫入本地資料庫中永久保存"""
        cls.init_database()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO runtime_logs (timestamp, log_level, message) VALUES (?, ?, ?)",
            (timestamp, level, message)
        )
        conn.commit()
        conn.close()
        print(f"💾 [資料庫記錄] 成功寫入日誌 [{level}]: {message}")

if __name__ == "__main__":
    # 測試寫入一筆系統啟動日誌
    DatabaseLogger.log_event("INFO", "Genesis-Core-Eternity 專案資料庫記錄模組測試成功。")

