import sqlite3
import urllib.request
import json
import datetime
import hashlib

DB_PATH = "genesis_core.db"
WAR_ROOM_PATH = "war_room.md"

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
    
    # 1. GitHub 趨勢探勘
    gh_url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence+created:>=2026-08-01&sort=stars&order=desc"
    req = urllib.request.Request(gh_url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            for item in data.get("items", [])[:4]:
                sources.append(("GitHub-AI", item.get("name"), item.get("html_url")))
    except Exception as e:
        print(f"[Debug] GitHub fetch error: {e}")

    # 2. Hugging Face 模型探勘
    hf_url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=4"
    req_hf = urllib.request.Request(hf_url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req_hf) as res:
            models = json.loads(res.read().decode('utf-8'))
            for m in models:
                sources.append(("HuggingFace", m.get("id"), f"https://huggingface.co/{m.get('id')}"))
    except Exception as e:
        print(f"[Debug] HuggingFace fetch error: {e}")
        
    return sources

def generate_war_room():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT cleaned_content FROM processed_assets ORDER BY id DESC LIMIT 8')
    rows = cursor.fetchall()
    conn.close()
    
    report = f"# 🌐 Genesis-Matrix 核心戰情室（War Room）\n"
    report += f"> **同步時間**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"> **狀態**：多源擴張運作中，資產庫零重複率 100%\n\n---\n\n"
    
    for r in rows:
        report += r[0] + "\n\n---\n\n"
        
    with open(WAR_ROOM_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[Expansion] 戰情室檔案已自動升級生成：{WAR_ROOM_PATH}")

def run():
    init_db()
    items = fetch_all_sources()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_added = 0
    for source, title, url in items:
        unique_str = f"{source}:{title}:{url}"
        h_id = get_hash(unique_str)
        
        cursor.execute('SELECT id FROM raw_intelligence WHERE hash_id = ?', (h_id,))
        if cursor.fetchone():
            continue
            
        cursor.execute('INSERT INTO raw_intelligence (source, title, url, hash_id) VALUES (?, ?, ?, ?)',
                       (source, title, url, h_id))
        intel_id = cursor.lastrowid
        
        asset_text = f"### 🚀 [{source}] {title}\n- **存取節點**: `{url}`\n- **維度狀態**: 已收編至自主情報庫 [Timestamp: {datetime.datetime.now().strftime('%H:%M:%S')}]"
        cursor.execute('INSERT INTO processed_assets (intel_id, cleaned_content) VALUES (?, ?)',
                       (intel_id, asset_text))
        new_added += 1
        
    conn.commit()
    conn.close()
    print(f"[Genesis-Matrix v4] 擴張掃描完畢。成功捕獲全新不重複資產：{new_added} 筆。")
    generate_war_room()

if __name__ == "__main__":
    run()
