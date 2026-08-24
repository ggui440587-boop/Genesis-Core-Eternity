import sqlite3

# ==============================================================
# System Mouth Module - 系統對外輸出與回報模組 (象徵嘴巴)
# ==============================================================

DB_NAME = "system_brain_memory.db"

def speak_and_report():
    """讀取頭部大腦的思考與感官記憶，並進行對外輸出回報"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # 查詢頭部的思考歷程
        cursor.execute("SELECT sensory_source, thought_content, created_at FROM head_thoughts ORDER BY id DESC LIMIT 3")
        thoughts = cursor.fetchall()
        conn.close()

        print("=" * 60)
        print(" 🗣️ 系統嘴巴 (輸出模組) - 開始對外發布與回報狀態")
        print("=" * 60)

        if not thoughts:
            print("（目前大腦沒有新訊息，嘴巴保持安靜。）")
        else:
            for t in thoughts:
                print(f"-> [發布報告] 來源: {t[0]} | 內容: {t[1]} | 時間: {t[2]}")

        print("=" * 60)
        print(" [狀態] 系統已成功完成：感知 -> 思考 -> 輸出的完整生命週期！")

    except Exception as e:
        print(f"[錯誤] 輸出模組執行失敗: {e}")

if __name__ == "__main__":
    speak_and_report()

