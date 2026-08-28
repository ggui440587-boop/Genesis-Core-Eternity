import sqlite3
import datetime

# ==============================================================
# System Head Module - 統整大腦與五官的系統頭部核心
# ==============================================================

DB_NAME = "system_brain_memory.db"

class SystemHead:
    def __init__(self):
        self.initialize_head_memory()

    def initialize_head_memory(self):
        """初始化頭部的核心記憶與思考結構"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
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
        print("[頭部核心] 腦波與記憶連結初始化完成。")

    def perceive_and_think(self, source, data):
        """模擬眼睛、耳朵等感官接收資訊後，交由大腦進行思考處理"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO head_thoughts (sensory_source, thought_content, processed_status) VALUES (?, ?, ?)",
            (source, data, "PROCESSED")
        )
        conn.commit()
        conn.close()
        print(f"[頭部思考] 接收來自 [{source}] 的訊息: 「{data}」 -> 大腦已完成解析與歸納。")

    def show_head_status(self):
        """顯示目前頭部大腦所接收並記憶的所有思考歷程"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT sensory_source, thought_content, created_at FROM head_thoughts ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        print("=" * 50)
        print(" 🧠 系統頭部 - 近期思考與感官記憶總覽")
        print("=" * 50)
        for r in rows:
            print(f"感官來源: {r[0]} | 內容: {r[1]} | 時間: {r[2]}")
        print("=" * 50)

if __name__ == "__main__":
    # 啟動頭部模組
    head = SystemHead()
    # 模擬感官輸入並讓頭部思考
    head.perceive_and_think("眼睛 (視覺)", "偵測到專案資料夾內有新的程式碼變動")
    head.perceive_and_think("耳朵 (聽覺)", "收到執行系統安全掃描的指令")
    # 顯示頭部思考狀態
    head.show_head_status()

