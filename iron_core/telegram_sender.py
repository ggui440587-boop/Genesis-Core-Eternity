import urllib.request
import json
import sqlite3

# 已經自動填入你的真實金鑰與 Chat ID
TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"

def send_latest_to_telegram():
    conn = sqlite3.connect("fusion_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, ai_summary, url FROM processed_items ORDER BY processed_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("[INFO] 沒有找到可推播的資料。")
        return

    title, summary, url = row
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    
    text = f"🔥 *Iron Core 智慧情報快遞*\n\n📌 *標題*：{title}\n\n💡 *AI 深度摘要*：\n{summary}\n\n🔗 *連結*：{url}"
    
    payload = json.dumps({
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }).encode('utf-8')

    try:
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("[SUCCESS] 成功將最新情報推送到你的 Telegram 手機！")
    except Exception as e:
        print(f"[ERROR] Telegram 發送失敗: {e}")

if __name__ == "__main__":
    send_latest_to_telegram()
