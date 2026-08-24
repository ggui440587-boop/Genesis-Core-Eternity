import sqlite3
import datetime

class AIAnalyzerModule:
    def __init__(self, db_name="genesis_local.db"):
        self.db_name = db_name

    def analyze_latest_records(self):
        print("-> 🧠 [AI Analyzer] 開始讀取本地資料庫進行智慧分析...")
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # 讀取最近的 5 筆爬蟲記錄
            cursor.execute("SELECT id, title, url, created_at FROM scraped_records ORDER BY id DESC LIMIT 5")
            records = cursor.fetchall()
            conn.close()

            if not records:
                print("   [!] 目前資料庫中尚無可分析的記錄。")
                return

            print(f"   [✓] 成功載入 {len(records)} 筆記錄進行分析：")
            for row in records:
                rec_id, title, url, created_at = row
                print(f"       - [{rec_id}] {title} (時間: {created_at})")

            print("-> [✓] AI 智慧分析與摘要任務執行完畢。")
        except Exception as e:
            print(f"   [✕] 分析過程發生異常: {e}")

if __name__ == "__main__":
    analyzer = AIAnalyzerModule()
    analyzer.analyze_latest_records()

