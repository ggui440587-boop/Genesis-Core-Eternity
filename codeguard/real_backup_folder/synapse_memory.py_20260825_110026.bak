import sqlite3
import datetime

# ==============================================================
# System Synapse & Long-term Memory Module - 長期記憶與突觸強化模組
# ==============================================================

DB_NAME = "system_brain_memory.db"

class SynapseMemory:
    def __init__(self):
        self.init_synapse_table()

    def init_synapse_table(self):
        """初始化長期記憶與突觸權重資料表"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_synapse_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experience_tag TEXT NOT NULL,
                success_weight INTEGER DEFAULT 1,
                learned_lesson TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[突觸記憶] 長期經驗資料庫與神經連結初始化完成。")

    def record_experience(self, tag, weight_delta, lesson):
        """記錄一筆新的系統執行經驗並強化突觸權重"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 檢查是否已有相同經驗標籤
        cursor.execute("SELECT id, success_weight FROM system_synapse_memory WHERE experience_tag = ?", (tag,))
        row = cursor.fetchone()

        if row:
            # 若存在則累加權重
            new_weight = row[1] + weight_delta
            cursor.execute("UPDATE system_synapse_memory SET success_weight = ?, learned_lesson = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                           (new_weight, lesson, row[0]))
            print(f"[突觸強化] 經驗標籤 [{tag}] 權重更新為: {new_weight}")
        else:
            # 若不存在則新增
            cursor.execute("INSERT INTO system_synapse_memory (experience_tag, success_weight, learned_lesson) VALUES (?, ?, ?)",
                           (tag, weight_delta, lesson))
            print(f"[突觸建立] 成功寫入全新長期經驗: [{tag}]")

        conn.commit()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print(" 🧠 系統長期記憶與突觸強化模組啟動")
    print("=" * 60)
    memory = SynapseMemory()
    memory.record_experience("AUTOMATION_TASK_OPTIMIZATION", 1, "批次非同步執行可有效降低系統負載")

