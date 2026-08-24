import sqlite3
from datetime import datetime
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

DB_PATH = "ai_media_hub.db"
STATIC_DIR = "static"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_tasks (
            id TEXT PRIMARY KEY,
            topic TEXT,
            script TEXT,
            video_path TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def render_video(task_id, topic):
    os.makedirs(STATIC_DIR, exist_ok=True)
    video_path = f"{STATIC_DIR}/{task_id}.mp4"
    try:
        cmd = [
            "ffmpeg", "-y", 
            "-f", "lavfi", "-i", "color=c=darkblue:s=720x1280:d=5",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
            "-vf", f"drawtext=text='{topic}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", video_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
    except Exception:
        pass
    return video_path

def run_once():
    init_db()
    topic = "Range Request Fixed Successfully"
    task_id = f"range_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    video_path = render_video(task_id, topic)
    
    cursor.execute('''
        INSERT INTO media_tasks (id, topic, script, video_path, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (task_id, topic, "支援 HTTP Range 斷點續傳，手機瀏覽器完美播放！", video_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

class RangeServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            path = self.path[1:]
            if os.path.exists(path):
                self.send_video_with_range(path)
                return
        
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
            <title>AI Media Studio - Range Fixed</title>
            <style>
                body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; margin: 0; }
                .card { background: #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #10b981; }
                video { width: 100%; max-height: 450px; border-radius: 6px; background: black; margin-top: 10px; }
                pre { white-space: pre-wrap; background: #090d16; padding: 10px; border-radius: 6px; color: #94a3b8; font-size: 0.85rem; }
            </style>
        </head>
        <body>
            <h2>🎬 AI 全媒體生產中心（影音串流完全版）</h2>
            <p>已支援 HTTP 範圍請求，手機點擊即可順暢播放影片。</p>
            <hr style="border-color: #334155;">
        """
        for r in rows:
            html += f"""
            <div class="card">
                <small style="color: #34d399;">{r[0]}</small>
                <h3>📌 {r[1]}</h3>
                <pre>{r[2]}</pre>
                <video controls playsinline preload="metadata"><source src="/{r[3]}" type="video/mp4"></video>
            </div>
            """
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

    def send_video_with_range(self, path):
        file_size = os.path.getsize(path)
        range_header = self.headers.get('Range', None)
        
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Type", "video/mp4")
        
        if range_header:
            m = re.search(r'bytes=(\d+)-(\d*)', range_header)
            if m:
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else file_size - 1
                length = end - start + 1
                
                self.send_response(206)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.end_headers()
                
                with open(path, 'rb') as f:
                    f.seek(start)
                    self.wfile.write(f.read(length))
                return
        
        self.send_response(200)
        self.send_header("Content-Length", str(file_size))
        self.end_headers()
        with open(path, 'rb') as f:
            self.wfile.write(f.read())

if __name__ == "__main__":
    run_once()
    HTTPServer(('0.0.0.0', 8080), RangeServerHandler).serve_forever()
