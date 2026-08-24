import urllib.request
import json
import sqlite3

# 請填入你的 Telegram Bot Token 與 Chat ID
TG_BOT_TOKEN = "你的_TELEGRAM_BOT_TOKEN"
TG_CHAT_ID = "你的_TELEGRAM_CHAT_ID"

def send_telegram_alert(title, summary, url):
    if not TG_BOT_TOKEN or TG_BOT_TOKEN.startswith("你的"):
        print("[INFO] Telegram Token 尚未設定，略過即時推播。")
        return
        
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    text = f"🔥 【Iron Core 智慧情報】\n\n📌 標題：{title}\n\n💡 AI 摘要：\n{summary}\n\n🔗 連結：{url}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": text}).encode('utf-8')
    
    try:
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("[SUCCESS] Telegram 推播發送成功！")
    except Exception as e:
        print(f"[ERROR] Telegram 推播失敗: {e}")

if __name__ == "__main__":
    # 測試推播最新的一筆資料庫內容
    try:
        conn = sqlite3.connect("fusion_hub.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, ai_summary, url FROM processed_items ORDER BY processed_at DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            send_telegram_alert(row[0], row[1], row[2])
        else:
            print("[INFO] 資料庫目前沒有資料可推播。")
    except Exception as e:
        print(f"[ERROR] 讀取資料庫失敗: {e}")
