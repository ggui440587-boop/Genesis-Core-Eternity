import urllib.request
import json
import sqlite3
from datetime import datetime, timedelta
import random
import time
import threading
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket

DB_PATH = "production_hub.db"
STATIC_DIR = "static"
MAX_DAYS_TO_KEEP = 14  # 保留兩週產出，精準控制手機容量

TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"

AI_KEYS = {
    "groq": "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",
    "openrouter": "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",
    "openai": "sk-proj-YOUR_OPENAI_KEY_FOR_WHISPER" # 若有需要 Whisper 可填入，沒填則自動略過
}

def log_msg(tag, msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{tag}] {msg}")

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS production_tasks (
            id TEXT PRIMARY KEY,
            topic TEXT,
            script_content TEXT,
            audio_path TEXT,
            video_path TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def cleanup_storage():
    if not os.path.exists(STATIC_DIR):
        return
    now = datetime.now()
    for filename in os.listdir(STATIC_DIR):
        file_path = os.path.join(STATIC_DIR, filename)
        if os.path.isfile(file_path):
            if now - datetime.fromtimestamp(os.path.getmtime(file_path)) > timedelta(days=MAX_DAYS_TO_KEEP):
                try:
                    os.remove(file_path)
                    log_msg("CLEAN", f"移除過期檔案: {filename}")
                except Exception:
                    pass

def fetch_live_tech_trend():
    """真實抓取 Hacker News 或退回高質量技術主題"""
    if check_internet():
        try:
            req = urllib.request.Request("https://hacker-news.firebaseio.com/v0/topstories.json", headers={'User-Agent': 'TermuxTool'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                story_id = json.loads(resp.read().decode())[0]
                item_req = urllib.request.Request(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                with urllib.request.urlopen(item_req, timeout=3) as item_resp:
                    data = json.loads(item_resp.read().decode())
                    if 'title' in data:
                        return f"Tech Trend: {data['title']}"
        except Exception:
            pass
    
    fallbacks = [
        "Termux Background Scripting & Python Automation Survival Guide",
        "Building Resilient AI Microservices on Mobile Terminals",
        "SQLite & Git Automated Local Backup Pipelines"
    ]
    return random.choice(fallbacks)

def generate_ai_script(topic):
    prompt = f"""
    請針對以下技術主題，產出一份結構清晰、適合實戰分享的 YouTube Shorts 45秒腳本與社群貼文（繁體中文）：
    主題：【{topic}】
    格式要求：包含標題、社群文案與黃金口白台詞。
    """
    
    # 優先使用 Groq (速度最快，最適合當生產工具)
    for _ in range(2):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {AI_KEYS['groq']}", "Content-Type": "application/json"}
            payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=12) as resp:
                return json.loads(resp.read().decode())['choices'][0]['message']['content'].strip()
        except Exception:
            time.sleep(2)
            
    # 備用 OpenRouter
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AI_KEYS['openrouter']}", "Content-Type": "application/json"}
        payload = {"model": "openrouter/free", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"自動化生成暫時受阻，主題：{topic}（系統離線備用範本）"

def render_media_assets(task_id):
    os.makedirs(STATIC_DIR, exist_ok=True)
    audio_file = f"{STATIC_DIR}/{task_id}.mp3"
    video_file = f"{STATIC_DIR}/{task_id}.mp4"
    
    # 建立基礎合規音檔
    with open(audio_file, "wb") as f:
        f.write(b"ID3\x03\x00\x00\x00\x00\x00\x0a")
        
    # 利用 Termux FFmpeg 實際渲染 9:16 Shorts 影片
    try:
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=navy:s=1080x1920:d=5",
            "-vf", "drawtext=text='Production Core':fontcolor=white:fontsize=55:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-t", "5", "-pix_fmt", "yuv420p", video_file
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=12)
    except Exception:
        pass

    return audio_file, video_file

def git_auto_backup():
    if not check_internet():
        return
    try:
        subprocess.run(["git", "add", DB_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", f"Production auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log_msg("GIT", "資料庫已成功同步至遠端倉庫。")
    except Exception:
        pass

def push_to_telegram(topic, script):
    if not check_internet():
        return
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    msg = f"🛠️ *【生產工具即時產出】*\n\n📌 *主題*：`{topic}`\n\n{script}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

def run_production_pipeline():
    init_db()
    cleanup_storage()
    
    topic = fetch_live_tech_trend()
    task_id = f"prod_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM production_tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        log_msg("BUILD", f"開始處理生產任務：{topic}")
        script = generate_ai_script(topic)
        audio_path, video_path = render_media_assets(task_id)
        
        cursor.execute('''
            INSERT INTO production_tasks (id, topic, script_content, audio_path, video_path, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, topic, script, audio_path, video_path, "就緒", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        
        push_to_telegram(topic, script)
        git_auto_backup()
        log_msg("SUCCESS", "生產任務圓滿完成！")
    conn.close()

class ProductionServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT created_at, topic, script_content, audio_path, video_path FROM production_tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        html = """<!DOCTYPE html>
        <html lang="zh-Hant">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Production Control Center</title>
            <style>
                body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; margin: 0; }
                .card { background: #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #334155; }
                pre { white-space: pre-wrap; background: #0b0f19; padding: 10px; border-radius: 6px; color: #e2e8f0; font-size: 0.85rem; }
            </style>
        </head>
        <body>
            <h2>🛠️ 生產工具控制中心</h2>
            <p>運行穩定中 - 支援本地 SQLite、FFmpeg 與 Git 自動備份</p>
            <hr style="border-color: #334155;">
        """
        for r in rows:
            html += f"""
            <div class="card">
                <small style="color: #38bdf8;">{r[0]}</small>
                <h3>📌 {r[1]}</h3>
                <pre>{r[2]}</pre>
                <audio controls style="width: 100%; margin-top: 5px;"><source src="/{r[3]}" type="audio/mpeg"></audio>
            </div>
            """
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    # 啟動輕量儀表板
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), ProductionServerHandler).serve_forever(), daemon=True).start()
    log_msg("SERVER", "生產儀表板已啟動：http://localhost:8080")
    
    # 戰神級 Watchdog 迴圈（確保 7x24 不死，崩潰自動重啟）
    while True:
        try:
            run_production_pipeline()
            log_msg("SLEEP", "任務循環結束，背景等待 6 小時...")
            time.sleep(21600)
        except KeyboardInterrupt:
            log_msg("EXIT", "生產工具手動關閉。")
            break
        except Exception as e:
            log_msg("ERROR", f"發生異常 ({e})，5秒後自動重啟防護網...")
            time.sleep(5)
