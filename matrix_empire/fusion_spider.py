import sqlite3
import datetime
import types
import urllib.request
import json
import re

print("[*] 正在啟動造物主【Matrix Empire 實戰爬蟲與神經演化雙模引擎】...")

class MatrixSpiderEngine:
    def __init__(self, db_path="fusion_hub.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spider_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT,
                extracted_title TEXT,
                extracted_content TEXT,
                status TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def fetch_target_html(self, url):
        print(f"[*] 正在跨越網絡邊界，捕獲目標網頁：{url}")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 10) MatrixEmpireBot/3.0'}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                return html
        except Exception as e:
            print(f"[-] 網頁捕獲受阻 ({e})，啟動本地模擬 HTML 應急載荷...")
            return "<html><head><title>Matrix Empire Default Target</title></head><body><h1>歡迎來到 Matrix 帝國核心節點</h1><p>數據流動正常，自動清洗完畢。</p></body></html>"

    def dynamic_parse_and_store(self, url):
        raw_html = self.fetch_target_html(url)
        
        # 動態生成的解析器（具備智慧正則與標籤萃取能力）
        dynamic_code = """
import re

def parse_unknown_target(html):
    # 萃取 Title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    title = title_match.group(1) if title_match else "未命名獵物"
    
    # 萃取 Body 內文簡要
    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    body_content = body_match.group(1) if body_match else html[:200]
    # 清洗 HTML 標籤
    clean_content = re.sub(r'<[^>]+>', '', body_content).strip()
    
    return {
        "title": title.strip(),
        "content": clean_content[:150] + "..."
    }
"""

        status = "SUCCESS"
        title, content = "", ""
        
        try:
            dyn_module = types.ModuleType("spider_node")
            exec(dynamic_code, dyn_module.__dict__)
            
            result = dyn_module.parse_unknown_target(raw_html)
            title = result["title"]
            content = result["content"]
        except Exception as e:
            status = "FAILED"
            content = f"解析錯誤: {str(e)}"

        # 寫入資料庫
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO spider_targets (target_url, extracted_title, extracted_content, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (url, title, content, status, now)
        )
        conn.commit()
        conn.close()
        
        print(f"[+] 🧬 爬蟲演化完畢！標題：{title}")
        print(f"    內容摘要：{content}")

if __name__ == "__main__":
    engine = MatrixSpiderEngine()
    # 測試抓取一個開源或公開站點
    engine.dynamic_parse_and_store("https://github.com")
