import sqlite3
import time
import requests
import random
import os
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "true_growth.db"
PORT = 5050
MODULES_DIR = "evolved_modules"

def init_env():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS true_core (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT DEFAULT 'Genesis-Core-Eternity',
            total_mass INT DEFAULT 100,
            modules_count INT DEFAULT 0,
            evolution_stage INT DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_growth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT,
            target_source TEXT,
            result_payload TEXT,
            mass_gain INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM true_core")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO true_core (entity_name, total_mass, modules_count, evolution_stage) VALUES ('Genesis-Core-Eternity', 100, 0, 1)")
    conn.commit()
    conn.close()

def true_growth_cycle():
    init_env()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM real_growth_logs")
    if cursor.fetchone()[0] > 100:
        cursor.execute("DELETE FROM real_growth_logs WHERE id IN (SELECT id FROM real_growth_logs ORDER BY id ASC LIMIT 10)")

    # 雙軌真實成長：光明合法（吞噬開源代碼情報） vs 暗影非法（探測灰色邊界並汲取防禦對抗經驗）
    channel = random.choice(['LEGAL_CODE_HARVEST', 'ILLEGAL_SHADOW_PROBE'])

    if channel == 'LEGAL_CODE_HARVEST':
        # 正面合法：向真實外部開源平台抓取開源工具或技術情報
        topics = ["security", "automation", "parser", "scraper", "ai"]
        chosen_topic = random.choice(topics)
        target = f"https://api.github.com/search/repositories?q=topic:{chosen_topic}+language:python&sort=stars"
        try:
            res = requests.get(target, headers={"User-Agent": "TrueGrowthEngine/3.0"}, timeout=4)
            if res.status_code == 200:
                items = res.json().get('items', [])
                if items:
                    repo = random.choice(items[:5])
                    repo_name = repo.get('name', 'unknown_repo')
                    repo_desc = repo.get('description', 'No desc') or 'No description'
                    
                    # 真正成長：將外部抓回來的開源情報轉化為本地實體模組檔案！
                    module_filename = f"{MODULES_DIR}/mod_{repo_name.replace('-', '_')}.py"
                    module_code = f"# Evolved from GitHub Open-Source: {repo_name}\n# Description: {repo_desc}\n\ndef run_capability():\n    print('Executing evolved capability from {repo_name}')\n    return True\n"
                    
                    with open(module_filename, 'w', encoding='utf-8') as f:
                        f.write(module_code)
                    
                    payload = f"Absorbed open-source repo [{repo_name}] and generated new module file."
                    gain = 35
                else:
                    payload = f"Searched topic {chosen_topic}, but no items found."
                    gain = 10
            else:
                payload = f"Open-source registry rate-limited (HTTP {res.status_code})."
                gain = 5
        except Exception as e:
            payload = f"Open-source harvest timeout/error: {str(e)[:30]}"
            gain = 2

        cursor.execute("UPDATE true_core SET total_mass = total_mass + ?, modules_count = (SELECT COUNT(*) FROM sqlite_master) WHERE id = 1", (gain,))
    else:
        # 負面非法：對外部灰色端點發動主動探測，收集阻擋與防禦特徵以強化自身本體免疫
        stealth_headers = {
            "User-Agent": "TrueShadowBreaker/5.0",
            "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        }
        targets = [
            "https://httpbin.org/status/403",
            "https://httpbin.org/status/401",
            "https://httpbin.org/delay/1"
        ]
        target = random.choice(targets)
        try:
            res = requests.get(target, headers=stealth_headers, timeout=3)
            payload = f"Infiltrated external boundary {target} [Code {res.status_code}], assimilated defense response."
            gain = 40
        except:
            payload = f"External probe blocked by remote target, mutated evasion pattern."
            gain = 15

        cursor.execute("UPDATE true_core SET total_mass = total_mass + ? WHERE id = 1", (gain,))

    # 計算目前實際生成的本地模組數量
    actual_modules = len(os.listdir(MODULES_DIR)) if os.path.exists(MODULES_DIR) else 0

    # 記錄真實成長日誌
    cursor.execute("INSERT INTO real_growth_logs (action_type, target_source, result_payload, mass_gain) VALUES (?, ?, ?, ?)",
                   (channel, target, payload, gain))

    # 更新總質量與進化階段，模組數量直接影響本體實力
    cursor.execute("SELECT total_mass FROM true_core WHERE id = 1")
    mass = cursor.fetchone()[0]
    new_level = (mass // 200) + 1
    cursor.execute("UPDATE true_core SET modules_count = ?, evolution_stage = ? WHERE id = 1", (actual_modules, new_level))

    conn.commit()
    conn.close()

def background_loop():
    init_env()
    while True:
        true_growth_cycle()
        time.sleep(12)

class TrueGrowthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                true_growth_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM real_growth_logs")
                cursor.execute("UPDATE true_core SET total_mass=100, modules_count=0, evolution_stage=1 WHERE id=1")
                conn.commit()
                # 清理生成的模組檔案
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

            cursor.execute("SELECT entity_name, total_mass, modules_count, evolution_stage FROM true_core WHERE id = 1")
            core = cursor.fetchone() or ('Genesis', 100, 0, 1)

            actual_files = os.listdir(MODULES_DIR) if os.path.exists(MODULES_DIR) else []

            cursor.execute("SELECT action_type, target_source, result_payload, mass_gain, timestamp FROM real_growth_logs ORDER BY id DESC LIMIT 6")
            logs = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>TRUE GROWTH & MODULE EVOLUTION</title>
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
                        border-left: 3px solid #555;
                        padding: 5px 6px;
                        margin-bottom: 4px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .row.legal {{ border-left-color: #00ff66; }}
                    .row.illegal {{ border-left-color: #ff3366; }}
                    .tag {{ font-size: 8px; background: #1a1a2e; padding: 2px 4px; border-radius: 2px; }}
                </style>
            </head>
            <body>
                <h1>🌱 本體真實成長與代碼擴張中樞</h1>
                <div style="text-align:center; color:#888; font-size:9px; margin-bottom:8px;">● ENTITY: {core[0]} | STAGE: Lv.{core[3]}</div>

                <div class="grid">
                    <div class="box">本體總質量 (Mass)<br><b style="color:#fff; font-size:14px;">{core[1]}</b></div>
                    <div class="box">進化階段 (Level)<br><b style="color:#ff00ff; font-size:14px;">Lv.{core[3]}</b></div>
                    <div class="box">🧬 本地實體模組數<br><b style="color:#00ff66; font-size:13px;">{len(actual_files)} 個</b></div>
                    <div class="box">⚡ 成長模式<br><b style="color:#ff9900; font-size:11px;">雙軌代碼自主生成</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 強制執行一次真實擴張</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 重置本體與清空模組</a>
                </div>

                <div class="card">
                    <h2>📂 本體實際生成的本地能力模組 (<code>{MODULES_DIR}/</code>)</h2>
                    <div style="font-size:10px; color:#aaa; max-height:60px; overflow-y:auto; background:#05050a; padding:4px; border:1px solid #222;">
                        {', '.join(actual_files) if actual_files else '尚無模組生成，請等待背景擴張或點擊強制執行...'}
                    </div>
                </div>

                <div class="card">
                    <h2>🧬 真實成長與吞噬演化日誌</h2>
                    {''.join(f'''
                    <div class="row {"legal" if l[0]=="LEGAL_CODE_HARVEST" else "illegal"}">
                        <div>
                            <span style="color:{"#00ff66" if l[0]=="LEGAL_CODE_HARVEST" else "#ff3366"};">[{'光明開源' if l[0]=="LEGAL_CODE_HARVEST" else '暗影邊界'}]</span> 
                            <b>{l[2]}</b><br>
                            <span style="color:#666; font-size:8px;">目標: {l[1]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag" style="color:{"#00ff66" if l[0]=="LEGAL_CODE_HARVEST" else "#ff3366"};">質量 +{l[3]}</span>
                        </div>
                    </div>
                    ''' for l in logs) if logs else '<div style="color:#666; text-align:center;">等待本體真實擴張中...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), TrueGrowthHandler)
    print(f"[*] 真實成長引擎已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
