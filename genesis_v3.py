import sqlite3
import urllib.request
import json
import datetime
import hashlib

DB_PATH = "genesis_core.db"
REPORT_PATH = "daily_report.md"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, title TEXT, url TEXT, hash_id TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intel_id INTEGER, cleaned_content TEXT,
            FOREIGN KEY (intel_id) REFERENCES raw_intelligence (id)
        )
    ''')
    conn.commit()
    conn.close()

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def fetch_all_sources():
    sources = []
    # GitHub
    gh_url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence+created:>=2026-08-01&sort=stars&order=desc"
    req = urllib.request.Request(gh_url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            for item in data.get("items", [])[:3]:
                sources.append(("GitHub", item.get("name"), item.get("html_url")))
    except Exception as e:
        print(f"[Debug] GitHub fetch error: {e}")

    # Hugging Face
    hf_url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=3"
    req_hf = urllib.request.Request(hf_url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req_hf) as res:
            models = json.loads(res.read().decode('utf-8'))
            for m in models:
                sources.append(("HuggingFace", m.get("id"), f"https://huggingface.co/{m.get('id')}"))
    except Exception as e:
        print(f"[Debug] HuggingFace fetch error: {e}")
        
    return sources

def run():
    init_db()
    items = fetch_all_sources()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_added = 0
    for source, title, url in items:
        unique_str = f"{source}:{title}:{url}"
        h_id = get_hash(unique_str)
        
        # 嚴格去重檢查
        cursor.execute('SELECT id FROM raw_intelligence WHERE hash_id = ?', (h_id,))
        if cursor.fetchone():
            continue
            
        cursor.execute('INSERT INTO raw_intelligence (source, title, url, hash_id) VALUES (?, ?, ?, ?)',
                       (source, title, url, h_id))
        intel_id = cursor.lastrowid
        
        asset_text = f"### [{source}] {title}\n- **Target**: {url}\n- **Status**: Verified Unique [Timestamp: {datetime.datetime.now()}]"
        cursor.execute('INSERT INTO processed_assets (intel_id, cleaned_content) VALUES (?, ?)',
                       (intel_id, asset_text))
        new_added += 1
        
    conn.commit()
    conn.close()
    print(f"[Genesis-Matrix v3] 執行完畢。過濾重複後，新增真實不重複資產：{new_added} 筆。")

if __name__ == "__main__":
    run()
