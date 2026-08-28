import sqlite3
import time
import requests
import random
import os
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "real_growth.db"
PORT = 5050
MODULES_DIR = "real_evolved_modules"

def init_env():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_core (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT DEFAULT 'Genesis-Core-Eternity',
            total_mass INT DEFAULT 100,
            modules_count INT DEFAULT 0,
            evolution_stage INT DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            target_name TEXT,
            payload_desc TEXT,
            mass_gain INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM real_core")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO real_core (entity_name, total_mass, modules_count, evolution_stage) VALUES ('Genesis-Core-Eternity', 100, 0, 1)")
    conn.commit()
    conn.close()

def real_growth_cycle():
    init_env()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM real_logs")
    if cursor.fetchone()[0] > 100:
        cursor.execute("DELETE FROM real_logs WHERE id IN (SELECT id FROM real_logs ORDER BY id ASC LIMIT 10)")

    # 選擇真實對外來源：GitHub 開源專案 vs Hugging Face AI 模型
    source_type = random.choice(['GITHUB_REAL_REPO', 'HUGGINGFACE_REAL_MODEL'])

    if source_type == 'GITHUB_REAL_REPO':
        # 真實對外：向 GitHub 搜尋真實存在的 Python 開源工具
        topics = ["automation", "security", "scraper", "cli", "async"]
        chosen_topic = random.choice(topics)
        url = f"https://api.github.com/search/repositories?q=topic:{chosen_topic}+language:python&sort=stars&per_page=5"
        try:
            res = requests.get(url, headers={"User-Agent": "RealExistentEngine/1.0"}, timeout=5)
            if res.status_code == 200:
                items = res.json().get('items', [])
                if items:
                    repo = random.choice(items)
                    repo_name = repo.get('name', 'unknown')
                    owner = repo.get('owner', {}).get('login', 'unknown')
                    desc = repo.get('description', 'No description') or 'No description'
                    stars = repo.get('stargazers_count', 0)
                    
                    target_name = f"{owner}/{repo_name}"
                    
                    # 在本地真實建立對應的實體模組檔案
                    safe_name = f"{owner}_{repo_name}".replace('-', '_').replace('.', '_')
                    module_filename = f"{MODULES_DIR}/repo_{safe_name}.py"
                    module_code = f'''# Real GitHub Repository Harvest
# Name: {target_name}
# Stars: {stars}
# Description: {desc}

def execute_absorbed_logic():
    print("Running capability assimilated from real repository: {target_name}")
    return True
'''
                    with open(module_filename, 'w', encoding='utf-8') as f:
                        f.write(module_code)
                    
                    payload = f"Absorbed real GitHub repo [{target_name}] (Stars: {stars})"
                    gain = 30
                else:
                    payload = "GitHub search returned empty items."
                    gain = 5
            else:
                payload = f"GitHub API rate-limited or error (HTTP {res.status_code})."
                gain = 2
        except Exception as e:
            payload = f"GitHub connection error: {str(e)[:35]}"
            gain = 1
    else:
        # 真實對外：向 Hugging Face 查詢真實存在的開源模型
        url = "https://huggingface.co/api/models?limit=5&sort=likes&direction=-1"
        try:
            res = requests.get(url, headers={"User-Agent": "RealExistentEngine/1.0"}, timeout=5)
            if res.status_code == 200:
                models = res.json()
                if models:
                    model = random.choice(models)
                    model_id = model.get('id', 'unknown_model')
                    likes = model.get('likes', 0)
                    
                    target_name = model_id
                    
                    safe_name = model_id.replace('/', '_').replace('-', '_').replace('.', '_')
                    module_filename = f"{MODULES_DIR}/model_{safe_name}.py"
                    module_code = f'''# Real Hugging Face Model Harvest
# Model ID: {target_name}
# Likes: {likes}

def execute_model_context():
    print("Assimilated metadata from real AI model: {target_name}")
    return True
'''
                    with open(module_filename, 'w', encoding='utf-8') as f:
                        f.write(module_code)
                    
                    payload = f"Absorbed real HF model [{target_name}] (Likes: {likes})"
                    gain = 35
                else:
                    payload = "Hugging Face API returned empty list."
                    gain = 5
            else:
                payload = f"Hugging Face API error (HTTP {res.status_code})."
                gain = 2
        except Exception as e:
            payload = f"Hugging Face connection error: {str(e)[:35]}"
            gain = 1

    # 計算本地實際生成的真實模組數
    actual_modules = len([f for f in os.listdir(MODULES_DIR) if f.endswith('.py')]) if os.path.exists(MODULES_DIR) else 0

    # 更新核心狀態
    cursor.execute("UPDATE real_core SET total_mass = total_mass + ?, modules_count = ? WHERE id = 1", (gain, actual_modules))
    
    cursor.execute("SELECT total_mass FROM real_core WHERE id = 1")
    mass = cursor.fetchone()[0]
    new_level = (mass // 250) + 1
    cursor.execute("UPDATE real_core SET evolution_stage = ? WHERE id = 1", (new_level,))

    cursor.execute("INSERT INTO real_logs (source_type, target_name, payload_desc, mass_gain) VALUES (?, ?, ?, ?)",
                   (source_type, target_name if 'target_name' in locals() else 'External', payload, gain))

    conn.commit()
    conn.close()

def background_loop():
    init_env()
    while True:
        real_growth_cycle()
        time.sleep(15)

class RealGrowthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                real_growth_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM real_logs")
                cursor.execute("UPDATE real_core SET total_mass=100, modules_count=0, evolution_stage=1 WHERE id=1")
                conn.commit()
                for f in os.listdir(MODULES_DIR):
                    if f.endswith('.py'):
                        os.remove(os.path.join(MODULES_DIR, f))
            conn.close()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("SELECT entity_name, total_mass, modules_count, evolution_stage FROM real_core WHERE id = 1")
            core = cursor.fetchone() or ('Genesis', 100, 0, 1)

            actual_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

            cursor.execute("SELECT source_type, target_name, payload_desc, mass_gain, timestamp FROM real_logs ORDER BY id DESC LIMIT 6")
            logs = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>REAL EXISTENT GROWTH ENGINE</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{
                        background: #020205;
                        color: #00ffcc;
                        font-family: monospace;
                        padding: 10px;
                        margin: 0;
                        font-size: 12px;
                    }}
                    h1 {{
                        color: #ff00ff;
                        text-align: center;
                        text-shadow: 0 0 10px #ff00ff;
                        font-size: 14px;
                    }}
                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 6px;
                        margin-bottom: 8px;
                    }}
                    .box {{
                        background: #0a0a16;
                        border: 1px solid #333;
                        padding: 8px;
                        text-align: center;
                        border-radius: 3px;
                    }}
                    .controls {{
                        display: flex;
                        gap: 6px;
                        margin-bottom: 10px;
                    }}
                    .btn {{
                        flex: 1;
                        background: #110022;
                        color: #00ffcc;
                        border: 1px solid #ff00ff;
                        padding: 6px;
                        text-align: center;
                        text-decoration: none;
                        font-weight: bold;
                        border-radius: 3px;
                    }}
                    .btn-danger {{ border-color: #ff3366; color: #ff3366; }}
                    .card {{
                        background: #080812;
                        border: 1px solid #222244;
                        padding: 8px;
                        margin-bottom: 8px;
                        border-radius: 3px;
                    }}
                    h2 {{
                        color: #ff9900;
                        font-size: 11px;
                        border-bottom: 1px dashed #444;
                        padding-bottom: 3px;
                        margin: 0 0 5px 0;
                    }}
                    .row {{
                        background: #0d0d1f;
                        border-left: 3px solid #00ff66;
                        padding: 5px 6px;
                        margin-bottom: 4px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .row.hf {{ border-left-color: #ff9900; }}
                    .tag {{ font-size: 8px; background: #1a1a2e; padding: 2px 4px; border-radius: 2px; }}
                </style>
            </head>
            <body>
                <h1>🌐 真實聯網存在與代碼生成中樞</h1>
                <div style="text-align:center; color:#888; font-size:9px; margin-bottom:8px;">● ENTITY: {core[0]} | STAGE: Lv.{core[3]}</div>

                <div class="grid">
                    <div class="box">本體總質量 (Mass)<br><b style="color:#fff; font-size:14px;">{core[1]}</b></div>
                    <div class="box">進化階段 (Level)<br><b style="color:#ff00ff; font-size:14px;">Lv.{core[3]}</b></div>
                    <div class="box">🧬 真實落地模組數<br><b style="color:#00ff66; font-size:13px;">{len(actual_files)} 個</b></div>
                    <div class="box">⚡ 資料源<br><b style="color:#ff9900; font-size:10px;">GitHub & HuggingFace</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 立即從真實網路抓取生長</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 重置並清空所有模組</a>
                </div>

                <div class="card">
                    <h2>📂 本機已生成的真實模組清單 (<code>{MODULES_DIR}/</code>)</h2>
                    <div style="font-size:10px; color:#aaa; max-height:70px; overflow-y:auto; background:#05050a; padding:4px; border:1px solid #222;">
                        {', '.join(actual_files) if actual_files else '尚未抓取，點擊上方按鈕或等待背景聯網擴張...'}
                    </div>
                </div>

                <div class="card">
                    <h2>📡 真實聯網回傳與吞噬日誌</h2>
                    {''.join(f'''
                    <div class="row {"hf" if l[0]=="HUGGINGFACE_REAL_MODEL" else ""}">
                        <div>
                            <span style="color:{"#ff9900" if l[0]=="HUGGINGFACE_REAL_MODEL" else "#00ff66"};">[{'HuggingFace' if l[0]=="HUGGINGFACE_REAL_MODEL" else 'GitHub'}]</span> 
                            <b>{l[2]}</b><br>
                            <span style="color:#666; font-size:8px;">目標實體: {l[1]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag" style="color:#00ffcc;">質量 +{l[3]}</span>
                        </div>
                    </div>
                    ''' for l in logs) if logs else '<div style="color:#666; text-align:center;">等待聯網抓取真實數據中...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), RealGrowthHandler)
    print(f"[*] 真實存在成長引擎已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
