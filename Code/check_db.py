import sqlite3

def view_tasks():
    conn = sqlite3.connect("fusion_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_id, status, created_at FROM video_tasks")
    rows = cursor.fetchall()
    print("\n--- 當前資料庫中的影片任務紀錄 ---")
    for row in rows:
        print(f"ID: {row[0]} | Task ID: {row[1]} | 狀態: {row[2]} | 建立時間: {row[3]}")
    conn.close()

if __name__ == "__main__":
    view_tasks()
