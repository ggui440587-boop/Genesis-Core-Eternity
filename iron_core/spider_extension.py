import urllib.request
import json
import sqlite3
from datetime import datetime

DB_PATH = "fusion_hub.db"
GITHUB_TOKEN = "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"

def fetch_real_github_trending():
    print("[SPIDER] 正在透過真實 GitHub Token 連線抓取熱門專案...")
    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"
    items = []
    try:
        headers = {
            'User-Agent': 'Termux-IronCore',
            'Authorization': f'Bearer {GITHUB_TOKEN}'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            for repo in data.get('items', [])[:3]:
                items.append({
                    "id": f"real_gh_{repo['id']}",
                    "source": "GitHubReal",
                    "title": repo['full_name'] + " | " + str(repo.get('description', '')),
                    "url": repo['html_url']
                })
    except Exception as e:
        print(f"[ERROR] GitHub 真實抓取失敗: {e}")
    return items

def save_extended_items(items):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    new_count = 0
    for item in items:
        cursor.execute("SELECT id FROM processed_items WHERE id = ?", (item['id'],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO processed_items (id, source, title, url, ai_summary, processed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item['id'], 
                item['source'], 
                item['title'], 
                item['url'], 
                "[等待真實 AI 運算]", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            new_count += 1
    conn.commit()
    conn.close()
    print(f"[SUCCESS] 成功存入 {new_count} 筆真實 GitHub 熱門情報！")

if __name__ == "__main__":
    items = fetch_real_github_trending()
    save_extended_items(items)
