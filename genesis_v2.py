import sqlite3
import urllib.request
import json
import datetime

DB_PATH = "genesis_core.db"
REPORT_PATH = "daily_report.md"

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

def fetch_github():
    """多源擴張：抓取 GitHub AI 開源專案"""
    url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence+created:>=2026-08-01&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            return [
                ("GitHub", item.get("name"), item.get("html_url"), f"Stars: {item.get('stargazers_count')} | {item.get('description', '')}")
                for item in data.get("items", [])[:2]
            ]
    except Exception as e:
        print(f"[Warning] GitHub 抓取異常: {e}")
        return []

def fetch_huggingface():
    """多源擴張：抓取 Hugging Face 熱門開源模型模型資訊"""
    url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=2"
    req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Matrix-Agent'})
    try:
        with urllib.request.urlopen(req) as res:
            models = json.loads(res.read().decode('utf-8'))
            return [
                ("HuggingFace", m.get("id"), f"https://huggingface.co/{m.get('id')}", f"Likes: {m.get('likes', 0)}")
                for m in models
            ]
    except Exception as e:
        print(f"[Warning] Hugging Face 抓取異常: {e}")
        return []

def run_pipeline():
    init_db()
    print(f"\n[Genesis-Matrix] === 多源情報與變現流引擎啟動: {datetime.datetime.now()} ===")
    
    # 1. 執行多源情報搜集
    raw_items = fetch_github() + fetch_huggingface()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_count = 0
    for source, title, url, raw_data in raw_items:
        # 檢查是否重複
        cursor.execute('SELECT id FROM raw_intelligence WHERE title = ?', (title,))
        if cursor.fetchone():
            continue
            
        # 寫入原始情報
        cursor.execute('''
            INSERT INTO raw_intelligence (source, title, url, raw_data)
            VALUES (?, ?, ?, ?)
        ''', (source, title, url, raw_data))
        intel_id = cursor.lastrowid
        
        # 2. 中游轉化：自動化內容變現流（轉化為社群貼文與短影音大綱）
        content_asset = f"""### 🔥 【{source} 爆款前沿】{title}
- **核心數據**：{raw_data}
- **直達連結**：[{url}]({url})
- 💡 **[自動化內容變現轉化]**
  - **社群貼文建議**：「今天發現一個超強的開源專案 {title}，亮點在於 {raw_data}！開發者們絕對不能錯過...」
  - **短影音腳本構思**：(30秒快節奏開場) 「如果你還不知道這個 AI 新模型/專案，那你可能要落後了！來看這個來自 {source} 的 {title}...」
"""
        cursor.execute('''
            INSERT INTO processed_assets (intel_id, category, cleaned_content)
            VALUES (?, ?, ?)
        ''', (intel_id, 'Monetization_Asset', content_asset))
        new_count += 1
        
    conn.commit()
    conn.close()
    print(f"[Processor] 多源整合完成！成功清洗並轉化 {new_count} 筆變現級數位資產。")
    
    # 3. 下游輸出
    generate_report()

def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT cleaned_content FROM processed_assets ORDER BY id DESC LIMIT 6')
    rows = cursor.fetchall()
    conn.close()
    
    report = f"# 🌐 Genesis-Matrix 全網流量與情報變現週報\n* 生成時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for r in rows:
        report += r[0] + "\n---\n"
        
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[Output] 變現級資產報告已自動生成：{REPORT_PATH}")

if __name__ == "__main__":
    run_pipeline()
