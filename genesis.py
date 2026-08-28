import sqlite3
import urllib.request
import json

DB_PATH = "genesis_core.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, title TEXT, url TEXT, raw_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intel_id INTEGER, category TEXT, cleaned_content TEXT, status TEXT DEFAULT 'ready',
            FOREIGN KEY (intel_id) REFERENCES raw_intelligence (id)
        )
    ''')
    conn.commit()
    conn.close()

def run_genesis_pipeline():
    init_db()
    print("[Genesis-Matrix] 正在連線至真實世界抓取開源情報...")
    
    url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence+created:>=2026-08-01&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])[:3] # 取前3筆
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            new_count = 0
            for item in items:
                title = item.get('name')
                html_url = item.get('html_url')
                description = item.get('description', 'No description')
                raw_text = f"Stars: {item.get('stargazers_count')} | Desc: {description}"
                
                # 寫入 raw
                cursor.execute('''
                    INSERT INTO raw_intelligence (source, title, url, raw_data)
                    VALUES (?, ?, ?, ?)
                ''', ('GitHub_Real', title, html_url, raw_text))
                intel_id = cursor.lastrowid
                
                # 立即清洗轉化 (Processor)
                cleaned_content = f"【AI 開源前沿速遞】\n專案名稱：{title}\n亮點：{raw_text}\n連結：{html_url}\n(自動化重構完成)"
                cursor.execute('''
                    INSERT INTO processed_assets (intel_id, category, cleaned_content)
                    VALUES (?, ?, ?)
                ''', (intel_id, 'OpenSource_AI', cleaned_content))
                new_count += 1
                
            conn.commit()
            conn.close()
            print(f"[Genesis-Matrix] 成功！已同步並清洗 {new_count} 筆真實專案，資料已存入資料庫。")
            
    except Exception as e:
        print(f"[Error] 執行異常: {e}")

if __name__ == "__main__":
    run_genesis_pipeline()

