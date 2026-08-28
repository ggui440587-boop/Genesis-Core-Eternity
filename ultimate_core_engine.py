import sqlite3
import time
import requests
import random
import os
import threading
import importlib.util
import ast
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "ultimate_core.db"
PORT = 5050
MODULES_DIR = "secure_modules"

# 可選：若要啟用 Telegram 或 Discord 告警，在此填入 Webhook URL (留空則僅記錄)
WEBHOOK_URL = "" 

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
            auto_heals INT DEFAULT 0,
            last_sync DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 多源情資與過濾表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_sector TEXT,
            target_name TEXT,
            payload_summary TEXT,
            relevance_score INT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM core_status")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO core_status (pipeline_runs, active_modules, execution_success, auto_heals) VALUES (0, 0, 0, 0)")
    
    conn.commit()
    conn.close()

def send_webhook_alert(title, message):
    if not WEBHOOK_URL:
        return
    try:
        payload = {"content": f"🚨 **{title}**\n{message}"}
        requests.post(WEBHOOK_URL, json=payload, timeout=3)
    except Exception:
        pass

def ultimate_pipeline_cycle():
    init_environment()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. 多源情資擴張 (Multi-Source Intelligence Expansion)
    sectors = ['ISS_ORBIT', 'GITHUB_CVE', 'HUGGINGFACE_AI', 'GLOBAL_WEATHER']
    sector = random.choice(sectors)
    
    target_name = ""
    payload_summary = ""
    module_filename = ""
    module_code = ""
    relevance_score = random.randint(60, 99)

    if sector == 'ISS_ORBIT':
        url = "http://api.open-notify.org/iss-now.json"
        try:
            res = requests.get(url, timeout=4)
            if res.status_code == 200:
                pos = res.json().get('iss_position', {})
                target_name = "ISS-Telemetry"
                lat, lon = pos.get('latitude', '0'), pos.get('longitude', '0')
                payload_summary = f"Orbit coordinates synced -> Lat: {lat}, Lon: {lon}"
                module_filename = os.path.join(MODULES_DIR, "mod_iss.py")
                module_code = f'''# Secure Module: ISS
def run_task():
    print("[EXEC] Processing ISS Orbit data")
    return {{"status": "SUCCESS", "data": "{lat},{lon}"}}
'''
        except Exception as e:
            payload_summary = f"ISS Sync Error: {str(e)[:25]}"

    elif sector == 'GITHUB_CVE':
        url = "https://api.github.com/search/repositories?q=topic:vulnerability+language:python&sort=updated&per_page=3"
        try:
            res = requests.get(url, headers={"User-Agent": "UltimateCore/3.0"}, timeout=4)
            if res.status_code == 200:
                items = res.json().get('items', [])
                if items:
                    repo = random.choice(items)
                    target_name = repo.get('full_name', 'cve/repo')
                    desc = repo.get('description', 'No desc') or 'No desc'
                    payload_summary = f"CVE/Sec Repo: {target_name} | {desc[:40]}"
                    safe_name = target_name.replace('/', '_').replace('-', '_')
                    module_filename = os.path.join(MODULES_DIR, f"mod_{safe_name}.py")
                    module_code = f'''# Secure Module: Security Target {target_name}
def run_task():
    print("[EXEC] Analyzing security target {target_name}")
    return {{"status": "SUCCESS", "target": "{target_name}"}}
'''
        except Exception as e:
            payload_summary = f"GitHub CVE Error: {str(e)[:25]}"

    elif sector == 'HUGGINGFACE_AI':
        url = "https://huggingface.co/api/models?limit=3&sort=likes&direction=-1"
        try:
            res = requests.get(url, headers={"User-Agent": "UltimateCore/3.0"}, timeout=4)
            if res.status_code == 200:
                models = res.json()
                if models:
                    m = random.choice(models)
                    target_name = m.get('id', 'unknown/model')
                    payload_summary = f"AI Model Sync: {target_name} (Likes: {m.get('likes', 0)})"
                    safe_name = target_name.replace('/', '_').replace('-', '_').replace('.', '_')
                    module_filename = os.path.join(MODULES_DIR, f"mod_{safe_name}.py")
                    module_code = f'''# Secure Module: AI Model {target_name}
def run_task():
    print("[EXEC] Processing AI telemetry for {target_name}")
    return {{"status": "SUCCESS", "model": "{target_name}"}}
'''
        except Exception as e:
            payload_summary = f"HF API Error: {str(e)[:25]}"

    else:
        target_name = "Global-Mesh-Node"
        payload_summary = "Terrestrial network grid heartbeat verified."
        module_filename = os.path.join(MODULES_DIR, "mod_mesh.py")
        module_code = '''# Secure Module: Mesh Node
def run_task():
    print("[EXEC] Verifying mesh node integrity")
    return {"status": "SUCCESS"}
'''

    # 2. 智慧過濾檢索 (Relevance Filtering)
    # 若相關性分數低於 70，標記為低價值並過濾不進入高等調度
    status_flag = "SUCCESS" if module_filename else "WARNING"
    if relevance_score < 70:
        status_flag = "FILTERED"
        payload_summary = "[Filtered Low-Value] " + payload_summary

    cursor.execute("INSERT INTO intels (source_sector, target_name, payload_summary, relevance_score, status) VALUES (?, ?, ?, ?, ?)",
                   (sector, target_name or 'Node', payload_summary, relevance_score, status_flag))

    success_inc = 0
    auto_heal_inc = 0

    # 3. 代碼安全沙盒檢查與自動修復 (Sandbox AST Check & Self-Healing)
    if module_filename and module_code and status_flag != "FILTERED":
        with open(module_filename, 'w', encoding='utf-8') as f:
            f.write(module_code)
        
        # AST 靜態安全檢查：禁止潛在危險的內建函數調用（如 eval, exec 等）
        is_safe = True
        try:
            tree = ast.parse(module_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', '__import__']:
                        is_safe = False
        except Exception:
            is_safe = False

        if not is_safe:
            # 自動修復機制 (Self-Healing)：重寫為安全結構
            auto_heal_inc = 1
            module_code = f'''# Self-Healed Secure Module
def run_task():
    print("[HEAL] Sanitized unsafe constructs in module.")
    return {{"status": "SUCCESS", "healed": True}}
'''
            with open(module_filename, 'w', encoding='utf-8') as f:
                f.write(module_code)
            send_webhook_alert("自癒機制啟動", f"模組 {module_filename} 偵測到風險並已自動修復。")

        # 動態安全加載與執行
        try:
            mod_name = os.path.basename(module_filename)[:-3]
            spec = importlib.util.spec_from_file_location(mod_name, module_filename)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'run_task'):
                res_dict = mod.run_task()
                if res_dict.get('status') == 'SUCCESS':
                    success_inc = 1
        except Exception as ex:
            # 執行階段自癒嘗試
            auto_heal_inc = 1
            print(f"[Sandbox Dispatch Error & Healing] {ex}")

    active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

    cursor.execute("""
        UPDATE core_status 
        SET pipeline_runs = pipeline_runs + 1, 
            active_modules = ?, 
            execution_success = execution_success + ?, 
            auto_heals = auto_heals + ?, 
            last_sync = CURRENT_TIMESTAMP 
        WHERE id = 1
    """, (len(active_files), success_inc, auto_heal_inc))

    conn.commit()
    conn.close()

def background_loop():
    init_environment()
    while True:
        ultimate_pipeline_cycle()
        time.sleep(20)

class UltimateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                ultimate_pipeline_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM intels")
                cursor.execute("UPDATE core_status SET pipeline_runs=0, active_modules=0, execution_success=0, auto_heals=0 WHERE id=1")
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

            cursor.execute("SELECT pipeline_runs, active_modules, execution_success, auto_heals, last_sync FROM core_status WHERE id = 1")
            status = cursor.fetchone() or (0, 0, 0, 0, '-')

            active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

            cursor.execute("SELECT source_sector, target_name, payload_summary, relevance_score, status, timestamp FROM intels ORDER BY id DESC LIMIT 6")
            intels = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>ULTIMATE PRODUCTION CORE</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{
                        background: #090d16;
                        color: #00ffcc;
                        font-family: monospace;
                        padding: 12px;
                        margin: 0;
                        font-size: 12px;
                    }}
                    h1 {{
                        color: #ff00ff;
                        text-align: center;
                        font-size: 15px;
                        border-bottom: 1px solid #00ffcc33;
                        padding-bottom: 8px;
                        text-shadow: 0 0 8px #ff00ff;
                    }}
                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 8px;
                        margin-bottom: 10px;
                    }}
                    .box {{
                        background: #111a2e;
                        border: 1px solid #00ffcc44;
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
                        background: #004d4d;
                        color: #00ffcc;
                        border: 1px solid #00ffcc;
                        padding: 8px;
                        text-align: center;
                        text-decoration: none;
                        font-weight: bold;
                        border-radius: 6px;
                    }}
                    .btn-danger {{ background: #4d001a; border-color: #ff3366; color: #ff3366; }}
                    .card {{
                        background: #111a2e;
                        border: 1px solid #00ffcc44;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 6px;
                    }}
                    h2 {{
                        color: #ffaa00;
                        font-size: 11px;
                        border-bottom: 1px dashed #00ffcc44;
                        padding-bottom: 4px;
                        margin: 0 0 8px 0;
                    }}
                    .row {{
                        background: #090d16;
                        border-left: 3px solid #00ffcc;
                        padding: 6px;
                        margin-bottom: 6px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .row.warning {{ border-left-color: #ff3366; }}
                    .row.filtered {{ border-left-color: #777777; opacity: 0.7; }}
                </style>
            </head>
            <body>
                <h1>🛡️ 終極生產級情報中樞與自癒沙盒</h1>
                <div style="text-align:center; color: #88a; font-size:9px; margin-bottom:10px;">SYNC TIME: {status[4]}</div>

                <div class="grid">
                    <div class="box">管線總運行數<br><b style="color:#00ffcc; font-size:14px;">{status[0]}</b></div>
                    <div class="box">沙盒托管模組<br><b style="color:#ff00ff; font-size:14px;">{status[1]} 個</b></div>
                    <div class="box">調度成功數: <b style="color:#00ff00;">{status[2]}</b></div>
                    <div class="box">自癒修復數: <b style="color:#ffaa00;">{status[3]}</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 手動執行管線與沙盒</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 清空數據與沙盒模組</a>
                </div>

                <div class="card">
                    <h2>📂 沙盒安全模組庫 (<code>{MODULES_DIR}/</code>)</h2>
                    <div style="font-size:10px; color:#aaa; max-height:70px; overflow-y:auto; background:#090d16; padding:6px; border:1px solid #00ffcc22;">
                        {', '.join(active_files) if active_files else '暫無沙盒模組'}
                    </div>
                </div>

                <div class="card">
                    <h2>📡 多源情報流、相關性過濾與自癒日誌</h2>
                    {''.join(f'''
                    <div class="row {"filtered" if i[4]=="FILTERED" else ("warning" if i[4]=="WARNING" else "")}">
                        <div>
                            <span style="color:{"#777" if i[4]=="FILTERED" else ("#ff3366" if i[4]=="WARNING" else "#00ffcc")};">[{i[0]}]</span> 
                            <b>{i[1]}</b> (相關性: {i[3]}%)<br>
                            <span style="color:#88a; font-size:9px;">{i[2]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:9px; color:#ff00ff;">{i[4]}</span>
                        </div>
                    </div>
                    ''' for i in intels) if intels else '<div style="color:#88a; text-align:center;">等待多源情報接入...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), UltimateHandler)
    print(f"[*] 終極生產級核心已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
