import urllib.request
import json
import sqlite3
import os
from datetime import datetime

DB_PATH = "fusion_hub.db"
TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"
GROQ_API_KEY = "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"
GITHUB_TOKEN = "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"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_items (
            id TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            url TEXT,
            ai_summary TEXT,
            processed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_sources():
    print("[ULTIMATE] 正在啟動多源情報全網掃描 (GitHub + Hacker News)...")
    items = []
    
    # 1. 抓取 GitHub 熱門專案
    try:
        gh_url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"
        headers = {'User-Agent': 'Termux-IronCore', 'Authorization': f'Bearer {GITHUB_TOKEN}'}
        req = urllib.request.Request(gh_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            for repo in data.get('items', [])[:2]:
                items.append({
                    "id": f"ult_gh_{repo['id']}",
                    "source": "GitHubUltimate",
                    "title": repo['full_name'] + " | " + str(repo.get('description', '')),
                    "url": repo['html_url']
                })
    except Exception as e:
        print(f"[WARNING] GitHub 抓取例外: {e}")

    # 2. 抓取 Hacker News 熱門
    try:
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(hn_url, headers={'User-Agent': 'Termux-IronCore'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            story_ids = json.loads(resp.read().decode())
            for s_id in story_ids[:2]:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                with urllib.request.urlopen(urllib.request.Request(item_url, headers={'User-Agent': 'Termux-IronCore'}), timeout=5) as r:
                    d = json.loads(r.read().decode())
                    if d and 'title' in d:
                        items.append({
                            "id": f"ult_hn_{s_id}",
                            "source": "HackerNews",
                            "title": d.get('title'),
                            "url": d.get('url', f"https://news.ycombinator.com/item?id={s_id}")
                        })
    except Exception as e:
        print(f"[WARNING] Hacker News 抓取例外: {e}")

    return items

def analyze_with_groq(title):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"請用精鍊的繁體中文，針對以下技術標題撰寫 50 字以內的技術摘要：{title}"}],
            "temperature": 0.5
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode())
            return res['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[解析降級] 標題：{title}"

def send_telegram(title, summary, url):
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    text = f"🚀 *Iron Core 終極情報快遞*\n\n📌 *標題*：{title}\n\n💡 *AI 深度摘要*：\n{summary}\n\n🔗 *連結*：{url}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[ERROR] TG 推播失敗: {e}")

def check_telegram_commands():
    """檢查 Telegram 聊天室指令，實現雙向互動！"""
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates"
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            for result in data.get('result', []):
                msg = result.get('message', {})
                text = msg.get('text', '')
                if text == '/status' or text == '/query':
                    # 回傳資料庫最新一筆給用戶
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT title, ai_summary FROM processed_items ORDER BY processed_at DESC LIMIT 1")
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        reply_text = f"📊 *系統戰利品狀態*\n📌 {row[0]}\n💡 {row[1]}"
                    else:
                        reply_text = "📊 目前資料庫尚無資料。"
                    
                    send_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
                    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": reply_text, "parse_mode": "Markdown"}).encode('utf-8')
                    urllib.request.urlopen(urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'}))
    except Exception as e:
        pass

def git_auto_backup():
    print("[BACKUP] 正在將最新資料與系統狀態備份至 GitHub...")
    os.system("git add fusion_hub.db iron_ultimate.py")
    os.system('git commit -m "Ultimate auto-sync state" > /dev/null 2>&1')
    os.system("git push origin main > /dev/null 2>&1")
    print("[SUCCESS] 雲端版本同步完畢！")

def main():
    init_db()
    # 1. 檢查 Telegram 是否有下達 /status 或 /query 指令
    check_telegram_commands()
    
    # 2. 多源抓取
    items = fetch_all_sources()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_items = []
    for item in items:
        cursor.execute("SELECT id FROM processed_items WHERE id = ?", (item['id'],))
        if not cursor.fetchone():
            print(f"[PROCESSING] 深度解析: {item['title']}")
            summary = analyze_with_groq(item['title'])
            cursor.execute('''
                INSERT INTO processed_items (id, source, title, url, ai_summary, processed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (item['id'], item['source'], item['title'], item['url'], summary, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            new_items.append((item['title'], summary, item['url']))
    conn.commit()
    conn.close()
    
    # 3. 發送推播
    for title, summary, url in new_items:
        send_telegram(title, summary, url)
        
    # 4. 自動備份上雲端
    git_auto_backup()
    print("[FINISH] 終極情報循環執行完畢！")

if __name__ == "__main__":
    main()
