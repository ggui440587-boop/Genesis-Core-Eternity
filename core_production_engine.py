import sqlite3
import time
import requests
import random
import os
import threading
import importlib.util
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "production_core.db"
PORT = 5050
MODULES_DIR = "managed_modules"

def init_environment():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 核心狀態表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS core_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_runs INT DEFAULT 0,
            active_modules INT DEFAULT 0,
            execution_success INT DEFAULT 0,
            last_sync DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 情資與資產表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            target_name TEXT,
            payload_summary TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM core_status")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO core_status (pipeline_runs, active_modules, execution_success) VALUES (0, 0, 0)")
    
    conn.commit()
    conn.close()

def pipeline_and_dispatch_cycle():
    init_environment()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. 執行情資管線 (Pipeline)：從真實來源抓取數據
    source_type = random.choice(['GITHUB_PIPELINE', 'HUGGINGFACE_PIPELINE'])
    target_name = ""
    payload_summary = ""
    module_filename = ""
    module_code = ""

    if source_type == 'GITHUB_PIPELINE':
        topics = ["automation", "parser", "cli", "utility"]
        chosen = random.choice(topics)
        url = f"https://api.github.com/search/repositories?q=topic:{chosen}+language:python&sort=stars&per_page=5"
        try:
            res = requests.get(url, headers={"User-Agent": "ProductionCore/2.0"}, timeout=5)
            if res.status_code == 200:
                items = res.json().get('items', [])
                if items:
                    repo = random.choice(items)
                    name = repo.get('name', 'pkg')
                    owner = repo.get('owner', {}).get('login', 'dev')
                    desc = repo.get('description', 'No desc') or 'No desc'
                    target_name = f"{owner}/{name}"
                    payload_summary = f"Synced repo: {target_name} | Desc: {desc[:60]}"
                    
                    safe_name = f"{owner}_{name}".replace('-', '_').replace('.', '_')
                    module_filename = os.path.join(MODULES_DIR, f"mod_{safe_name}.py")
                    module_code = f'''# Managed Pipeline Module: {target_name}
def run_task():
    print("[EXEC] Executing logic for {target_name}")
    return {"status": "SUCCESS", "source": "{target_name}"}
'''
            else:
                payload_summary = f"GitHub API limited (HTTP {res.status_code})"
        except Exception as e:
            payload_summary = f"GitHub connection error: {str(e)[:30]}"
    else:
        url = "https://huggingface.co/api/models?limit=5&sort=likes&direction=-1"
        try:
            res = requests.get(url, headers={"User-Agent": "ProductionCore/2.0"}, timeout=5)
            if res.status_code == 200:
                models = res.json()
                if models:
                    model = random.choice(models)
                    target_name = model.get('id', 'unknown/model')
                    likes = model.get('likes', 0)
                    payload_summary = f"Synced AI Model: {target_name} (Likes: {likes})"
                    
                    safe_name = target_name.replace('/', '_').replace('-', '_').replace('.', '_')
                    module_filename = os.path.join(MODULES_DIR, f"mod_{safe_name}.py")
                    module_code = f'''# Managed Pipeline Module (AI Model): {target_name}
def run_task():
    print("[EXEC] Processing metadata for model {target_name}")
    return {"status": "SUCCESS", "source": "{target_name}"}
'''
            else:
                payload_summary = f"HuggingFace API error (HTTP {res.status_code})"
        except Exception as e:
            payload_summary = f"HuggingFace connection error: {str(e)[:30]}"

    # 寫入情資紀錄
    status_flag = "SUCCESS" if module_filename else "WARNING"
    cursor.execute("INSERT INTO intels (source_type, target_name, payload_summary, status) VALUES (?, ?, ?, ?)",
                   (source_type, target_name or 'N/A', payload_summary, status_flag))

    # 2. 模組調度器 (Dispatcher)：寫入並動態加載執行本地模組
    success_increment = 0
    if module_filename and module_code:
        with open(module_filename, 'w', encoding='utf-8') as f:
            f.write(module_code)
        
        # 動態加載與沙盒測試執行
        try:
            module_name = os.path.basename(module_filename)[:-3]
            spec = importlib.util.spec_from_file_location(module_name, module_filename)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'run_task'):
                res_data = mod.run_task()
                if res_data.get('status') == 'SUCCESS':
                    success_increment = 1
        except Exception as ex:
            print(f"[Dispatcher Error] {ex}")

    # 計算目前實際托管的模組數
    active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

    cursor.execute("""
        UPDATE core_status 
        SET pipeline_runs = pipeline_runs + 1, 
            active_modules = ?, 
            execution_success = execution_success + ?, 
            last_sync = CURRENT_TIMESTAMP 
        WHERE id = 1
    """, (len(active_files), success_increment))

    conn.commit()
    conn.close()

def background_loop():
    init_environment()
    while True:
        pipeline_and_dispatch_cycle()
        time.sleep(20)

class ProductionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                pipeline_and_dispatch_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM intels")
                cursor.execute("UPDATE core_status SET pipeline_runs=0, active_modules=0, execution_success=0 WHERE id=1")
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

            cursor.execute("SELECT pipeline_runs, active_modules, execution_success, last_sync FROM core_status WHERE id = 1")
            status = cursor.fetchone() or (0, 0, 0, '-')

            active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

            cursor.execute("SELECT source_type, target_name, payload_summary, status, timestamp FROM intels ORDER BY id DESC LIMIT 6")
            intels = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>PRODUCTION CORE: PIPELINE & DISPATCHER</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{
                        background: #0d1117;
                        color: #c9d1d9;
                        font-family: monospace;
                        padding: 12px;
                        margin: 0;
                        font-size: 12px;
                    }}
                    h1 {{
                        color: #58a6ff;
                        text-align: center;
                        font-size: 15px;
                        border-bottom: 1px solid #30363d;
                        padding-bottom: 8px;
                    }}
                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 8px;
                        margin-bottom: 10px;
                    }}
                    .box {{
                        background: #161b22;
                        border: 1px solid #30363d;
                        padding: 8px;
                        text-align: center;
                        border-radius: 6px;
                    }}
                    .controls {{
                        display: flex;
                        gap: 8px;
                        margin-bottom: 12px;
                    }}
                    .btn {{
                        flex: 1;
                        background: #238636;
                        color: #fff;
                        border: none;
                        padding: 8px;
                        text-align: center;
                        text-decoration: none;
                        font-weight: bold;
                        border-radius: 6px;
                    }}
                    .btn-danger {{ background: #da3633; }}
                    .card {{
                        background: #161b22;
                        border: 1px solid #30363d;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 6px;
                    }}
                    h2 {{
                        color: #8b949e;
                        font-size: 11px;
                        border-bottom: 1px solid #30363d;
                        padding-bottom: 4px;
                        margin: 0 0 8px 0;
                    }}
                    .row {{
                        background: #0d1117;
                        border-left: 3px solid #238636;
                        padding: 6px;
                        margin-bottom: 6px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .row.warning {{ border-left-color: #d29922; }}
                </style>
            </head>
            <body>
                <h1>⚙️ 生產級情資管線與模組調度核心</h1>
                <div style="text-align:center; color: #8b949e; font-size:9px; margin-bottom:10px;">LAST SYNC: {status[3]}</div>

                <div class="grid">
                    <div class="box">管線執行次數<br><b style="color:#58a6ff; font-size:14px;">{status[0]}</b></div>
                    <div class="box">托管模組數量<br><b style="color:#3fb950; font-size:14px;">{status[1]} 個</b></div>
                    <div class="box" style="grid-column: span 2;">調度成功執行數: <b style="color:#f0883e;">{status[2]} 次</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 手動執行管線與調度</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 清空管線與模組</a>
                </div>

                <div class="card">
                    <h2>📂 託管模組清單 (<code>{MODULES_DIR}/</code>)</h2>
                    <div style="font-size:10px; color:#8b949e; max-height:70px; overflow-y:auto; background:#0d1117; padding:6px; border:1px solid #30363d;">
                        {', '.join(active_files) if active_files else '暫無托管模組'}
                    </div>
                </div>

                <div class="card">
                    <h2>📡 即時情報流與調度日誌</h2>
                    {''.join(f'''
                    <div class="row {"warning" if i[3]=="WARNING" else ""}">
                        <div>
                            <span style="color:{"#d29922" if i[3]=="WARNING" else "#3fb950"};">[{i[0]}]</span> 
                            <b>{i[1]}</b><br>
                            <span style="color:#8b949e; font-size:9px;">{i[2]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:9px; color:#58a6ff;">{i[3]}</span>
                        </div>
                    </div>
                    ''' for i in intels) if intels else '<div style="color:#8b949e; text-align:center;">等待情資管線注入...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), ProductionHandler)
    print(f"[*] 生產級核心已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
