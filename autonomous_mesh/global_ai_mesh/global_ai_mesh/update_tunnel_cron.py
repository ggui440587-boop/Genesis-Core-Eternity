with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 升級伺服器，加入自動排程與背景循環觸發點
cron_injection = """
# === 自動排程與背景自主演化循環 ===
import threading
import time

def background_autonomous_loop():
    while True:
        try:
            # 模擬背景自動化情報擴張與變現掃描
            time.sleep(60) # 每60秒執行一次循環
        except Exception as e:
            pass

# 啟動背景執行緒
threading.Thread(target=background_autonomous_loop, daemon=True).start()
"""

if "background_autonomous_loop" not in code:
    code = cron_injection + "\n" + code
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully injected Autonomous Cron Loop!")
else:
    print("Cron loop already exists.")
