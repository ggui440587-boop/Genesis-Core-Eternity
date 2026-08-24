import sqlite3
import time
import os

# ==============================================================
# Micro Circulation & Immune Module - 微觀循環與免疫防護 (模擬血球與血管)
# ==============================================================

DB_NAME = "system_brain_memory.db"

class MicroCirculationSystem:
    @staticmethod
    def white_blood_cell_scan():
        """白血球模組：掃描系統資料庫與環境，檢查是否有異常或未處理的錯誤"""
        print("[白血球免疫] 正在巡邏血管與骨架，檢查系統健康狀態...")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # 檢查是否有異常的任務狀態
            cursor.execute("SELECT COUNT(*) FROM head_thoughts WHERE processed_status = 'PENDING'")
            pending_count = cursor.fetchone()[0]
            conn.close()

            if pending_count > 0:
                print(f"[白血球警報] 發現 {pending_count} 筆待處理的思考節點，準備進行清理或交辦。")
            else:
                print("[白血球正常] 系統內部環境健康，無異常感染或堆積。")
        except Exception as e:
            print(f"[白血球防禦] 偵測到異常，觸發血小板修復機制: {e}")
            MicroCirculationSystem.platelet_repair()

    @staticmethod
    def platelet_repair():
        """血小板模組：當系統或資料庫發生輕微受損時進行修復"""
        print("[血小板修復] 正在進行系統傷口凝固與資料表自我修復...")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # 確保基礎資料表結構完整
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
        print("[血小板修復] 修復完成，資料通道已恢復正常。")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🩸 系統微觀循環與免疫系統啟動")
    print("=" * 60)
    MicroCirculationSystem.white_blood_cell_scan()

