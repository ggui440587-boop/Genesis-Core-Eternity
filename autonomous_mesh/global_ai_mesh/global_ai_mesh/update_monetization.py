with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 升級伺服器，加入 Telegram 推播模組與自動化變現管線掛載點
monetization_injection = """
# === 自動化內容變現與 Telegram 推播模組 ===
import urllib.request
import json

def send_telegram_alert(message):
    # 讀取環境變數或預設安全略過
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return "Telegram API 未設定（已安全略過）"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return "Telegram 推播成功"
    except Exception as e:
        return f"Telegram 推播失敗: {str(e)}"
"""

if "send_telegram_alert" not in code:
    code = monetization_injection + "\n" + code
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully injected Monetization & Telegram pipeline!")
else:
    print("Monetization pipeline already exists.")
