import sqlite3
import datetime
import json

# ==============================================================
# Polyglot DB Bridge - 多語言通用資料庫相容與統整模組
# ==============================================================

class PolyglotDBBridge:
    DB_NAME = "genesis_runtime_logs.db"

    @classmethod
    def init_universal_database(cls):
        """建立支援多語言（Python/JS/C++/Java/Rust）寫入的通用資料表"""
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS polyglot_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_source TEXT,
                timestamp TEXT,
                log_level TEXT,
                payload_data TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("-> 🟢 [資料庫相容] 多語言通用資料表初始化完成！")

    @classmethod
    def write_log_from_language(cls, language_name, level, message):
        """提供給各語言（或其橋接端）統一寫入資料庫的標準介面"""
        cls.init_universal_database()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        payload = json.dumps({"message": message}, ensure_ascii=False)

        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO polyglot_logs (language_source, timestamp, log_level, payload_data) VALUES (?, ?, ?, ?)",
            (language_name, timestamp, level, payload)
        )
        conn.commit()
        conn.close()
        print(f"💾 [{language_name} 兼容寫入] 成功將狀態存入通用資料庫: {message}")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🌐 [資料庫總相容測試] 模擬各語言寫入通用資料庫...")
    print("=" * 60)

    # 模擬各語言寫入測試
    PolyglotDBBridge.write_log_from_language("Python", "INFO", "核心守護進程運行正常。")
    PolyglotDBBridge.write_log_from_language("Node.js", "INFO", "跨語言設定讀取完畢。")
    PolyglotDBBridge.write_log_from_language("C++", "SUCCESS", "記憶體底層診斷通過。")
    PolyglotDBBridge.write_log_from_language("Java", "SUCCESS", "JVM 企業級模組掛載成功。")
    PolyglotDBBridge.write_log_from_language("Rust", "SUCCESS", "記憶體安全檢查無誤。")

    print("=" * 60)

