import urllib.request
import json
import sqlite3
from datetime import datetime

DB_PATH = "fusion_hub.db"
TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"
GROQ_API_KEY = "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"

def init_empire_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_empire (
            id TEXT PRIMARY KEY,
            type TEXT,
            title TEXT,
            content TEXT,
            proposal TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_market_leads():
    """模擬全網高價值技術外包與變現機會"""
    print("[EMPIRE] 正在掃描高價值市場案源與流量素材...")
    leads = [
        {
            "id": "emp_lead_01",
            "type": "外包案源",
            "title": "Need Python Automation & Termux Expert for Data Pipeline",
            "description": "Looking for someone to build a robust data scraper that runs reliably on mobile/Linux environments with automated database sync."
        },
        {
            "id": "emp_content_01",
            "type": "自媒體吸粉",
            "title": "Build Your Own Autonomous AI Agent in Termux",
            "description": "Exploring how to run LLM-powered background agents on Android devices using Python and SQLite."
        }
    ]
    return leads

def generate_ai_business_assets(title, desc, item_type):
    """利用 Groq AI 同時生成行銷文案與專業接案提案 (Proposal)"""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        
        if item_type == "外包案源":
            prompt = f"針對以下外包案源，請幫我寫一份專業、自信且具說服力的英文接案提案信 (Proposal)，展示我們具備 Termux 與 Python 自動化實力：\n專案標題：{title}\n描述：{desc}"
        else:
            prompt = f"請將以下技術主題改寫成一篇吸引科技愛好者點閱、具備強大傳播力的自媒體短貼文（繁體中文）：\n標題：{title}\n描述：{desc}"

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode())
            return res['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"AI 產出降級內容：{desc}"

def send_empire_alert(item_type, title, result_text):
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    emoji = "💼" if item_type == "外包案源" else "🚀"
    text = f"{emoji} *【商業帝國雷達】* [{item_type}]\n\n📌 *標題*：{title}\n\n💡 *AI 生成成果 (提案信/貼文草稿)*：\n{result_text}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[ERROR] 商業推播失敗: {e}")

def main():
    init_empire_db()
    leads = fetch_market_leads()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for lead in leads:
        cursor.execute("SELECT id FROM business_empire WHERE id = ?", (lead['id'],))
        if not cursor.fetchone():
            print(f"[PROCESSING] 正在為 [{lead['type']}] 打造變現資產：{lead['title']}")
            ai_asset = generate_ai_business_assets(lead['title'], lead['description'], lead['type'])
            
            cursor.execute('''
                INSERT INTO business_empire (id, type, title, content, proposal, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (lead['id'], lead['type'], lead['title'], lead['description'], ai_asset, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            
            # 即時推送到手機 Telegram
            send_empire_alert(lead['type'], lead['title'], ai_asset)
            
    conn.close()
    print("[SUCCESS] 商業帝國循環執行完畢，所有變現資產已送達手機！")

if __name__ == "__main__":
    main()
