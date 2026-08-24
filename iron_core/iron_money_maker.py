import urllib.request
import json
import sqlite3
from datetime import datetime

DB_PATH = "fusion_hub.db"
TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"
GROQ_API_KEY = "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"

def init_money_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS money_leads (
            id TEXT PRIMARY KEY,
            category TEXT,
            title TEXT,
            content TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_freelance_leads():
    """模擬/抓取真實技術接案與變現機會（案源雷達）"""
    print("[MONEY] 正在掃描全網高價值案源與變現機會...")
    # 這裡鎖定高利潤的自動化、AI 串接、Python 專案需求
    leads = [
        {
            "id": "lead_001",
            "category": "接案商機",
            "title": "急需 Python 自動化爬蟲工程師（預算優渥）",
            "content": "客戶需要一個每日自動抓取競品資料並同步到資料庫的 Termux/Linux 腳本，具備長期維護意願。"
        },
        {
            "id": "lead_002",
            "category": "自媒體變現",
            "title": "AI 應用趨勢電子報主題素材",
            "content": "分析當前最夯的開源 AI Agent 發展，可直接改寫為 500 字自媒體深度貼文，吸引科技粉與導流。"
        }
    ]
    return leads

def generate_monetization_copy(title, raw_content):
    """利用 Groq AI 將情報轉化為具備行銷與變現力的文案"""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"請將以下主題改寫成一篇吸引眼球、具備專業商業價值的自媒體短貼文或接案評估報告，繁體中文：\n標題：{title}\n內容：{raw_content}"}],
            "temperature": 0.7
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode())
            return res['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"商業文案生成降級：{raw_content}"

def send_money_alert(category, title, copy):
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    text = f"💰 *【商業變現雷達】* [{category}]\n\n📌 *專案/主題*：{title}\n\n✍️ *AI 生成變現文案/商機解析*：\n{copy}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[ERROR] 賺錢雷達推播失敗: {e}")

def main():
    init_money_db()
    leads = fetch_freelance_leads()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for lead in leads:
        cursor.execute("SELECT id FROM money_leads WHERE id = ?", (lead['id'],))
        if not cursor.fetchone():
            print(f"[PROCESSING] 正在提煉變現價值: {lead['title']}")
            ai_copy = generate_monetization_copy(lead['title'], lead['content'])
            cursor.execute('''
                INSERT INTO money_leads (id, category, title, content, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (lead['id'], lead['category'], lead['title'], ai_copy, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            
            # 即時推送到 Telegram 手機
            send_money_alert(lead['category'], lead['title'], ai_copy)
            
    conn.close()
    print("[SUCCESS] 賺錢雷達掃描完畢，高價值商機已推送到你的手機！")

if __name__ == "__main__":
    main()
