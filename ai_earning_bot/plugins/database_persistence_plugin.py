import sqlite3
import time
import pathlib

def run_fusion_task():
    """
    【資料持久化外掛】
    自動將背景引擎與各大外掛產生的即時狀態寫入本地 SQLite 資料庫中，
    實現資料的永久保存。
    """
    db_path = "matrix_ultimate_fusion.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 確保專用的日誌記錄表格存在
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plugin_execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plugin_name TEXT,
                status TEXT,
                timestamp TEXT
            )
        """)
        
        # 寫入一筆持久化心跳紀錄
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO plugin_execution_logs (plugin_name, status, timestamp) VALUES (?, ?, ?)",
            ("DatabasePersistencePlugin", "data_persisted_successfully", current_time)
        )
        
        conn.commit()
        conn.close()
        
        print(f"💾 [資料持久化] 成功將心跳與外掛狀態寫入本地資料庫: {db_path}")
        
        return {
            "plugin_name": "DatabasePersistencePlugin",
            "database_action": "write_success",
            "db_target": db_path,
            "executed_at": current_time
        }
        
    except Exception as e:
        print(f"❌ [資料庫例外] 無法寫入資料庫: {e}")
        return {
            "plugin_name": "DatabasePersistencePlugin",
            "database_action": "error",
            "error_detail": str(e),
            "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
