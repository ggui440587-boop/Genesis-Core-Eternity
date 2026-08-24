import sqlite3
import time
import re
import requests
from bs4 import BeautifulSoup

class MatrixFactory:
    def __init__(self, db_name="matrix_intel.db", content_output="generated_posts.md"):
        self.db_name = db_name
        self.content_output = content_output
        self.init_database()
        print("[Matrix-Factory] 智庫與內容生產工廠已開機...")

    def init_database(self):
        """初始化本地 SQLite 智庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intel_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                link TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def ingest_logs_to_db(self, log_file="web3_code_wealth.log"):
        """將主雷達的 log 讀取並結構化存入 SQLite"""
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"[Matrix-Factory] 找不到日誌檔 {log_file}，請先確保主雷達運行。")
            return

        entries = re.findall(r'\[(.*?)\] (.*?) \(通道: (.*?)\)', content)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        added_count = 0
        for source, title, link in entries:
            title = title.strip()
            link = link.strip()
            
            # 簡單分類
            category = "General"
            lower_t = title.lower()
            if any(kw in lower_t for kw in ["crypto", "bitcoin", "defi", "blockchain", "yield", "airdrop"]):
                category = "Crypto & Web3"
            elif any(kw in lower_t for kw in ["ai", "claude", "agent", "voice", "python", "github", "tool"]):
                category = "AI & OpenSource"
            elif any(kw in lower_t for kw in ["invest", "earn", "money", "job"]):
                category = "Wealth & Business"

            # 檢查是否已存在
            cursor.execute("SELECT id FROM intel_vault WHERE link = ?", (link,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO intel_vault (source, title, link, category) VALUES (?, ?, ?, ?)",
                    (source, title, link, category)
                )
                added_count += 1

        conn.commit()
        conn.close()
        print(f"[Matrix-Factory] 成功將 {added_count} 筆新情報結構化存入 SQLite 資料庫！")

    def generate_content_scripts(self):
        """從資料庫萃取高價值項目，自動生成短影音與文章腳本"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # 取出最近 5 筆高品質的 AI 或 區塊鏈項目
        cursor.execute("SELECT title, link, category FROM intel_vault ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("[Matrix-Factory] 資料庫目前尚無資料可供轉換。")
            return

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        markdown_output = f"# 🚀 智慧內容工廠：自動化腳本生成報表\n\n> 生成時間: {timestamp}\n\n---\n\n"

        for idx, (title, link, category) in enumerate(rows, 1):
            # 自動化生成短影音/貼文腳本結構
            markdown_output += f"## 🎬 專案 {idx}: {title}\n"
            markdown_output += f"- **分類**: `{category}`\n- **原始通道**: {link}\n\n"
            markdown_output += f"### 💡 短影音 / 社群貼文腳本範本：\n"
            markdown_output += f"> **[Hook 開場白]**：「大家都在找的強大神器！今天這支影片帶你看懂這個在 GitHub 爆紅的專案——`{title[:40]}`！」\n\n"
            markdown_output += f"> **[Core 核心亮點]**：這個工具專為 `{category}` 設計，能幫你大幅省下時間、拉開與其他人的資訊差。\n\n"
            markdown_output += f"> **[Call to Action 結尾引導]**：「想了解詳細安裝或原始碼的大師，連結已經放在留言區，馬上點進去解鎖你的數位武器！」\n\n"
            markdown_output += f"---\n\n"

        with open(self.content_output, "w", encoding="utf-8") as f:
            f.write(markdown_output)

        print(f"[Matrix-Factory] 內容生產完畢！短影音與文章腳本已儲存至 {self.content_output}")

if __name__ == "__main__":
    factory = MatrixFactory()
    factory.ingest_logs_to_db()
    factory.generate_content_scripts()

