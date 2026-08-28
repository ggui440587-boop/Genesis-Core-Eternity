import sqlite3
import datetime

class ProjectScraperModule:
    def __init__(self, db_name="genesis_local.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("-> [✓] 本地 SQLite 資料庫初始化完成。")

    def fetch_and_store(self, title, url):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO scraped_records (title, url, created_at) VALUES (?, ?, ?)", 
                       (title, url, timestamp))
        conn.commit()
        conn.close()
        print(f"-> [✓] 成功儲存資料記錄: {title}")

if __name__ == "__main__":
    scraper = ProjectScraperModule()
    scraper.fetch_and_store("Genesis Core Sample", "https://github.com/ggui440587-boop/Genesis-Core-Eternity")

