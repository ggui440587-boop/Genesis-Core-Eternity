import sqlite3
import time
import requests
import random
import os
import threading
import hashlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "external_expansion.db"
PORT = 5050

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 對外情報與內化資產表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS external_intel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direction TEXT,
            target_endpoint TEXT,
            intel_payload TEXT,
            power_harvest INT,
            risk_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 系統演化狀態表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS core_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_harvests INT DEFAULT 0,
            legal_power INT DEFAULT 100,
            illegal_power INT DEFAULT 100,
            evolution_stage INT DEFAULT 1
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM core_status")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO core_status (total_harvests, legal_power, illegal_power, evolution_stage) VALUES (0, 100, 100, 1)")
    conn.commit()
    conn.close()

def external_expansion_engine():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 清理舊情報，保持高速
    cursor.execute("SELECT COUNT(*) FROM external_intel")
    if cursor.fetchone()[0] > 100:
        cursor.execute("DELETE FROM external_intel WHERE id IN (SELECT id FROM external_intel ORDER BY id ASC LIMIT 10)")

    # 隨機選擇對外擴張方向：合法光明端 vs 非法暗影端
    direction = random.choice(['LEGAL_OUTBOUND', 'ILLEGAL_OUTBOUND'])

    if direction == 'LEGAL_OUTBOUND':
        # 正面合法對外：對接外部公開 API、開源情報、公開數據庫
        legal_targets = [
            "https://api.github.com/search/repositories?q=topic:cybersecurity&sort=stars",
            "https://api.github.com/search/repositories?q=topic:artificial-intelligence&sort=stars",
            "https://httpbin.org/json"
        ]
        target = random.choice(legal_targets)
        try:
            res = requests.get(target, headers={"User-Agent": "GlobalLegalScraper/4.0"}, timeout=3)
            if res.status_code == 200:
                payload = f"Successfully harvested public OSINT metadata from {target.split('/')[2]}"
                harvest = 20
                risk = "LOW"
            else:
                payload = f"Legal target {target.split('/')[2]} returned status {res.status_code}"
                harvest = 5
                risk = "MINIMAL"
        except:
            payload = f"Legal outbound connection to {target.split('/')[2]} timed out."
            harvest = -5
            risk = "TIMEOUT"
        
        cursor.execute("UPDATE core_status SET total_harvests = total_harvests + 1, legal_power = legal_power + ? WHERE id = 1", (harvest,))
    else:
        # 負面非法對外：主動探測外部灰色端點、違規狀態、防禦禁區
        stealth_headers = {
            "User-Agent": "ShadowOutbound-Breaker/9.0",
            "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        }
        illegal_targets = [
            "https://httpbin.org/status/403",
            "https://httpbin.org/status/401",
            "https://httpbin.org/status/500",
            "https://httpbin.org/delay/1"
        ]
        target = random.choice(illegal_targets)
        try:
            res = requests.get(target, headers=stealth_headers, timeout=2)
            payload = f"Infiltrated external gray/restricted endpoint {target} [Code {res.status_code}]"
            harvest = 35
            risk = "HIGH"
        except:
            payload = f"External infiltration probe to {target} blocked by remote firewall."
            harvest = 10
            risk = "CRITICAL"

        cursor.execute("UPDATE core_status SET total_harvests = total_harvests + 1, illegal_power = illegal_power + ? WHERE id = 1", (harvest,))

    # 記錄對外情報並內化吞噬
    cursor.execute("INSERT INTO external_intel (direction, target_endpoint, intel_payload, power_harvest, risk_level) VALUES (?, ?, ?, ?, ?)",
                   (direction, target, payload, harvest, risk))

    # 檢查是否達到進化門檻
    cursor.execute("SELECT total_harvests FROM core_status WHERE id = 1")
    total = cursor.fetchone()[0]
    if total % 10 == 0:
        cursor.execute("UPDATE core_status SET evolution_stage = evolution_stage + 1 WHERE id = 1")

    conn.commit()
    conn.close()

def background_loop():
    init_db()
    while True:
        external_expansion_engine()
        time.sleep(10)

class ExternalMatrixHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                external_expansion_engine()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM external_intel")
                cursor.execute("UPDATE core_status SET total_harvests=0, legal_power=100, illegal_power=100, evolution_stage=1 WHERE id=1")
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

            cursor.execute("SELECT total_harvests, legal_power, illegal_power, evolution_stage FROM core_status WHERE id = 1")
            status = cursor.fetchone() or (0, 100, 100, 1)

            cursor.execute("SELECT direction, target_endpoint, intel_payload, power_harvest, risk_level, timestamp FROM external_intel ORDER BY id DESC LIMIT 6")
            intels = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>EXTERNAL EXPANSION MATRIX</title>
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
                <h1>🌐 對外雙軌情資擴張與進化中樞</h1>
                <div style="text-align:center; color:#888; font-size:9px; margin-bottom:8px;">● MULTI-SOURCE OUTBOUND EXPANSION & ASSIMILATION</div>

                <div class="grid">
                    <div class="box">總擴張次數: <b style="color:#fff;">{status[0]}</b></div>
                    <div class="box">進化階段: <b style="color:#ff00ff;">Lv.{status[3]}</b></div>
                    <div class="box">🟢 正面合法抓取力<br><b style="color:#00ff66; font-size:13px;">{status[1]}</b></div>
                    <div class="box">🔴 負面非法吞噬力<br><b style="color:#ff3366; font-size:13px;">{status[2]}</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 立即觸發對外擴張</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 重置擴張數據</a>
                </div>

                <div class="card">
                    <h2>📡 外部情資雙軌回傳與內化日誌</h2>
                    {''.join(f'''
                    <div class="row {"legal" if i[0]=="LEGAL_OUTBOUND" else "illegal"}">
                        <div>
                            <span style="color:{"#00ff66" if i[0]=="LEGAL_OUTBOUND" else "#ff3366"};">[{'合法公開' if i[0]=="LEGAL_OUTBOUND" else '非法暗影'}]</span> 
                            <b>{i[2]}</b><br>
                            <span style="color:#666; font-size:8px;">目標: {i[1]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag" style="color:{"#00ff66" if i[4]=="LOW" else "#ff3366"};">{i[4]}</span><br>
                            <span style="color:#aaa; font-size:8px;">威力 +{i[3]}</span>
                        </div>
                    </div>
                    ''' for i in intels) if intels else '<div style="color:#666; text-align:center;">等待對外情報回傳中...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), ExternalMatrixHandler)
    print(f"[*] 對外情資擴張中樞已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
