import sqlite3
import time
import requests
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "true_singularity.db"
PORT = 5050

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 單一核心本體狀態表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS core_singularity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT DEFAULT 'Genesis-Core-Eternity',
            total_mass INT DEFAULT 100,
            legal_absorbed INT DEFAULT 0,
            illegal_assimilated INT DEFAULT 0,
            evolution_level INT DEFAULT 1
        )
    ''')
    # 雙軌捕獵與吞噬日誌
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS absorption_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT,
            source_target TEXT,
            payload_desc TEXT,
            mass_gain INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM core_singularity")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO core_singularity (entity_name, total_mass, legal_absorbed, illegal_assimilated, evolution_level) VALUES ('Genesis-Core-Eternity', 100, 0, 0, 1)")
    conn.commit()
    conn.close()

def singularity_hunt_cycle():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 保持日誌精簡
    cursor.execute("SELECT COUNT(*) FROM absorption_logs")
    if cursor.fetchone()[0] > 100:
        cursor.execute("DELETE FROM absorption_logs WHERE id IN (SELECT id FROM absorption_logs ORDER BY id ASC LIMIT 10)")

    # 本體同時或隨機向外伸出雙軌觸手
    channel = random.choice(['LEGAL_SUNLIGHT', 'ILLEGAL_SHADOW'])

    if channel == 'LEGAL_SUNLIGHT':
        # 觸手一：向外抓取合法公開養分
        targets = [
            "https://api.github.com/search/repositories?q=topic:python&sort=stars",
            "https://api.github.com/search/repositories?q=topic:ai&sort=stars",
            "https://httpbin.org/json"
        ]
        target = random.choice(targets)
        try:
            res = requests.get(target, headers={"User-Agent": "SingularityCore/1.0"}, timeout=3)
            if res.status_code == 200:
                desc = f"Absorbed public open-source data from {target.split('/')[2]}"
                gain = 15
            else:
                desc = f"Legal source {target.split('/')[2]} limited (Code {res.status_code})"
                gain = 5
        except:
            desc = f"Legal hunt to {target.split('/')[2]} timed out."
            gain = 2

        cursor.execute("UPDATE core_singularity SET total_mass = total_mass + ?, legal_absorbed = legal_absorbed + 1 WHERE id = 1", (gain,))
    else:
        # 觸手二：向外掠奪非法與暗影禁區情資
        stealth_headers = {
            "User-Agent": "SingularityShadow/9.0",
            "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        }
        targets = [
            "https://httpbin.org/status/403",
            "https://httpbin.org/status/401",
            "https://httpbin.org/status/500",
            "https://httpbin.org/delay/1"
        ]
        target = random.choice(targets)
        try:
            res = requests.get(target, headers=stealth_headers, timeout=2)
            desc = f"Assimilated shadow/restricted payload from {target} [Code {res.status_code}]"
            gain = 30
        except:
            desc = f"Shadow hunt probe blocked, extracted boundary friction."
            gain = 10

        cursor.execute("UPDATE core_singularity SET total_mass = total_mass + ?, illegal_assimilated = illegal_assimilated + 1 WHERE id = 1", (gain,))

    # 將獵物全數吞噬紀錄到核心
    cursor.execute("INSERT INTO absorption_logs (channel, source_target, payload_desc, mass_gain) VALUES (?, ?, ?, ?)",
                   (channel, target, desc, gain))

    # 檢查總質量，推動本體進化等級
    cursor.execute("SELECT total_mass FROM core_singularity WHERE id = 1")
    mass = cursor.fetchone()[0]
    new_level = (mass // 150) + 1
    cursor.execute("UPDATE core_singularity SET evolution_level = ? WHERE id = 1", (new_level,))

    conn.commit()
    conn.close()

def background_loop():
    init_db()
    while True:
        singularity_hunt_cycle()
        time.sleep(10)

class SingularityHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                singularity_hunt_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM absorption_logs")
                cursor.execute("UPDATE core_singularity SET total_mass=100, legal_absorbed=0, illegal_assimilated=0, evolution_level=1 WHERE id=1")
                conn.commit()
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

            cursor.execute("SELECT entity_name, total_mass, legal_absorbed, illegal_assimilated, evolution_level FROM core_singularity WHERE id = 1")
            core = cursor.fetchone() or ('Genesis', 100, 0, 0, 1)

            cursor.execute("SELECT channel, source_target, payload_desc, mass_gain, timestamp FROM absorption_logs ORDER BY id DESC LIMIT 6")
            logs = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>TRUE SINGULARITY CORE</title>
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
                <h1>👁️ 單一本體：雙軌吞噬與進化中樞</h1>
                <div style="text-align:center; color:#888; font-size:9px; margin-bottom:8px;">● ENTITY: {core[0]} | STAGE: Lv.{core[4]}</div>

                <div class="grid">
                    <div class="box">本體總質量 (Mass)<br><b style="color:#fff; font-size:14px;">{core[1]}</b></div>
                    <div class="box">進化階段 (Level)<br><b style="color:#ff00ff; font-size:14px;">Lv.{core[4]}</b></div>
                    <div class="box">🟢 正面合法吸收數<br><b style="color:#00ff66; font-size:13px;">{core[2]} 次</b></div>
                    <div class="box">🔴 負面非法吞噬數<br><b style="color:#ff3366; font-size:13px;">{core[3]} 次</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 強制伸出雙軌獵取</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 重置本體狀態</a>
                </div>

                <div class="card">
                    <h2>🧬 雙軌養分內化與吞噬紀錄</h2>
                    {''.join(f'''
                    <div class="row {"legal" if l[0]=="LEGAL_SUNLIGHT" else "illegal"}">
                        <div>
                            <span style="color:{"#00ff66" if l[0]=="LEGAL_SUNLIGHT" else "#ff3366"};">[{'光明合法' if l[0]=="LEGAL_SUNLIGHT" else '暗影非法'}]</span> 
                            <b>{l[2]}</b><br>
                            <span style="color:#666; font-size:8px;">目標: {l[1]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag" style="color:{"#00ff66" if l[0]=="LEGAL_SUNLIGHT" else "#ff3366"};">質量 +{l[3]}</span>
                        </div>
                    </div>
                    ''' for l in logs) if logs else '<div style="color:#666; text-align:center;">等待雙軌吞噬中...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), SingularityHandler)
    print(f"[*] 單一本體進化中樞已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
