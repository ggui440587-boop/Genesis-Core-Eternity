import sqlite3
import json
import os

class KnowledgeDatabaseEngine:
    def __init__(self, db_name="knowledge_matrix.db"):
        self.db_name = db_name
        self._init_table()

    def _init_table(self):
        """初始化內建模組資料表結構"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                payload TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def insert_record(self, category, data_dict):
        """將資料以 JSON 字串形式寫入資料庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        payload_str = json.dumps(data_dict, ensure_ascii=False)
        cursor.execute(
            "INSERT INTO knowledge_records (category, payload) VALUES (?, ?)",
            (category, payload_str)
        )
        conn.commit()
        conn.close()
        print(f"-> 💾 [知識庫] 已成功寫入分類 [{category}] 的資料。")

    def fetch_all_records(self):
        """提取資料庫中的所有紀錄"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, payload, timestamp FROM knowledge_records;")
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "category": row[1],
                "payload": json.loads(row[2]),
                "timestamp": row[3]
            })
        return results

if __name__ == "__main__":
    # 測試執行與示範
    engine = KnowledgeDatabaseEngine()
    engine.insert_record("SystemCore", {"status": "Active", "version": "1.0.0"})
    
    print("\n-> 📋 目前知識庫中的所有紀錄：")
    for rec in engine.fetch_all_records():
        print(rec)
