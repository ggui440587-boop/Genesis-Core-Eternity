import time
import sqlite3
import os

# ==============================================================
# Genesis-Core-Eternity 主控生態系 (統整所有身體與系統模組)
# ==============================================================

DB_NAME = "system_brain_memory.db"

def initialize_entire_system():
    """初始化整個系統的資料庫與骨架"""
    print("=" * 60)
    print(" 🚀 正在啟動 Genesis-Core-Eternity 自動化生態系...")
    print("=" * 60)

    # 1. 建立骨架與記憶資料庫
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_skeleton_spine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_name TEXT NOT NULL,
            data_payload TEXT,
            status TEXT DEFAULT 'ACTIVE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS head_thoughts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensory_source TEXT,
            thought_content TEXT,
            processed_status TEXT DEFAULT 'PENDING',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("[系統啟動] 骨架、大腦記憶與感官通道建構完成。")

def run_ecosystem_loop():
    """執行系統的主循環生命週期"""
    initialize_entire_system()

    print("\n[系統運轉] 生態系進入常駐背景運行狀態 (按 Ctrl + C 可安全退出)...")
    try:
        cycle = 1
        while True:
            print("-" * 50)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 生態系第 {cycle} 個運作循環：")

            # 模擬感官輸入與大腦思考
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO head_thoughts (sensory_source, thought_content) VALUES (?, ?)", 
                           ("環境感知", f"第 {cycle} 次心跳週期狀態正常"))
            conn.commit()
            conn.close()

            print("-> [心臟與神經] 動力源穩定，免疫系統巡邏中...")

            cycle += 1
            time.sleep(5)  # 每 5 秒一個循環

    except KeyboardInterrupt:
        print("\n[系統關閉] 收到中斷訊號，生態系安全停止運作。")

if __name__ == "__main__":
    run_ecosystem_loop()

