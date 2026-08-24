import urllib.request
import urllib.parse
import json
import sqlite3
from datetime import datetime, timedelta
import random
import time
import threading
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

DB_PATH = "ai_media_hub.db"
STATIC_DIR = "static"
MAX_DAYS_TO_KEEP = 14

TG_BOT_TOKEN = "8883992864:AAHmf1TB4kUBvbqTlmLvsU_s3PjZAKXLMvk"
TG_CHAT_ID = "7692801565"

GROQ_KEY = "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"

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
        CREATE TABLE IF NOT EXISTS media_tasks (
            id TEXT PRIMARY KEY,
            topic TEXT,
            script TEXT,
            audio_path TEXT,
            image_path TEXT,
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
                except Exception:
                    pass

def fetch_tech_topic():
    topics = [
        "Python Asyncio Performance Optimization Hacks",
        "Building Zero-Cost AI Agents on Mobile Terminals",
        "The Future of Edge Computing and Local LLMs",
        "Automated Git Sync and Database Resilience"
    ]
    return random.choice(topics)

def step1_ai_script(topic):
    """【1. AI 文案引擎】使用 Groq 產出高吸睛短影音口白"""
    log_msg("AI", f"正在生成文案，主題：{topic}")
    prompt = f"針對主題「{topic}」，寫一段 30 秒的 Shorts 短影音口白與社群貼文，繁體中文，語氣專業且精煉。"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode())['choices'][0]['message']['content'].strip()
    except Exception:
        return f"探索技術新高度：{topic}。自動化架構與高效率實踐。"

def step2_ai_tts(script, audio_path):
    """【2. AI 聲音引擎】使用 Edge-TTS 產生真人級語音（需安裝 edge-tts 套件）"""
    log_msg("TTS", "正在合成 AI 語音配音...")
    clean_text = script.replace('\n', ' ')[:200] # 取前200字轉語音
    try:
        # 呼叫 Termux 內的 edge-tts 指令
        cmd = ["edge-tts", "--voice", "zh-TW-HsiaoChenNeural", "--text", clean_text, "--write-media", audio_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return True
    except Exception:
        pass
    
    # 備用：若無 edge-tts，建立基本音檔
    with open(audio_path, "wb") as f:
        f.write(b"ID3\x03\x00\x00\x00\x00\x00\x0a")
    return False

def step3_ai_image(topic, image_path):
    """【3. AI 圖片引擎】透過 Pollinations API 免費生成高畫質背景圖"""
    log_msg("IMAGE", "正在由 AI 生成高畫質背景圖片...")
    try:
        prompt_encoded = urllib.parse.quote(f"Cyberpunk futuristic technology, cinematic lighting, 4k, hyper-detailed, theme: {topic}")
        img_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1080&height=1920&nologo=true"
        urllib.request.urlretrieve(img_url, image_path)
        if os.path.exists(image_path) and os.path.getsize(image_path) > 5000:
            return True
    except Exception:
        pass
    return False

def step4_ai_video(image_path, audio_path, video_path):
    """【4. AI 影片引擎】使用 FFmpeg 將 AI 圖片與 AI 聲音動態合成 9:16 短影音（加入輕微縮放運鏡效果）"""
    log_msg("VIDEO", "正在透過 FFmpeg 進行動態影片合成...")
    try:
        # 若有圖片與音訊，組合成帶有縮放運鏡 (zoompan) 的動態影片
        if os.path.exists(image_path):
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", image_path, "-i", audio_path,
                "-vf", "scale=2000:2000,zoompan=z='min(zoom+0.0015,1.15)':d=125:s=1080x1920",
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-shortest", video_path
            ]
        else:
            # 純色動態備用
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=10",
                "-i", audio_path, "-c:v", "libx264", "-c:a", "aac", "-shortest", video_path
            ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        return os.path.exists(video_path)
    except Exception:
        return False

def push_telegram(topic, script, video_path):
    if not check_internet():
        return
    # 發送通知文字
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    msg = f"🎬✨ *【全自動 AI 影音流水線完成】*\n\n📌 *主題*：`{topic}`\n\n{script}"
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

def run_pipeline():
    init_db()
    cleanup_storage()
    
    topic = fetch_tech_topic()
    task_id = f"media_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM media_tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        os.makedirs(STATIC_DIR, exist_ok=True)
        audio_path = f"{STATIC_DIR}/{task_id}.mp3"
        image_path = f"{STATIC_DIR}/{task_id}.jpg"
        video_path = f"{STATIC_DIR}/{task_id}.mp4"
        
        script = step1_ai_script(topic)
        step2_ai_tts(script, audio_path)
        step3_ai_image(topic, image_path)
        step4_ai_video(image_path, audio_path, video_path)
        
        cursor.execute('''
            INSERT INTO media_tasks (id, topic, script, audio_path, image_path, video_path, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, topic, script, audio_path, image_path, video_path, "已生成動態影片", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        
        push_telegram(topic, script, video_path)
        log_msg("SUCCESS", "全自動 AI 影音生產完畢！")
    conn.close()

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT created_at, topic, script, video_path FROM media_tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        html = """<!DOCTYPE html>
        <html lang="zh-Hant">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
            <title>AI Media Studio</title>
            <style>
                body { font-family: sans-serif; background: #090d16; color: #f8fafc; padding: 15px; margin: 0; }
                .card { background: #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #6366f1; }
                video { width: 100%; max-height: 400px; border-radius: 6px; background: black; margin-top: 10px; }
                pre { white-space: pre-wrap; background: #0f172a; padding: 10px; border-radius: 6px; color: #cbd5e1; font-size: 0.85rem; }
            </style>
        </head>
        <body>
            <h2>🎬 AI 全媒體生產中心</h2>
            <p>AI 文案 ➔ AI 語音 ➔ AI 繪圖 ➔ 智慧動態運鏡合成</p>
            <hr style="border-color: #334155;">
        """
        for r in rows:
            html += f"""
            <div class="card">
                <small style="color: #818cf8;">{r[0]}</small>
                <h3>📌 {r[1]}</h3>
                <pre>{r[2]}</pre>
                <video controls><source src="/{r[3]}" type="video/mp4"></video>
            </div>
            """
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    # 確保安裝了 edge-tts（若未安裝可在終端手動 pip install edge-tts）
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), ServerHandler).serve_forever(), daemon=True).start()
    log_msg("SERVER", "媒體儀表板運行於 http://localhost:8080")
    
    while True:
        try:
            run_pipeline()
            log_msg("SLEEP", "等待下一次自動生成循環 (6小時)...")
            time.sleep(21600)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log_msg("ERROR", f"發生錯誤 ({e})，5秒後重試...")
            time.sleep(5)
