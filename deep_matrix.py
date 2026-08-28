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

DB_FILE = "deep_cyber_matrix.db"
PORT = 5050

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 節點核心表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            pathway TEXT,
            profession TEXT,
            credits INT DEFAULT 100,
            health INT DEFAULT 100,
            mutation_level INT DEFAULT 1,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 雙軌內化記憶庫（合法 vs 非法）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assimilated_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT,
            data_source TEXT,
            payload_hash TEXT,
            power_gain INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 動態防禦與免疫日誌
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS defense_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            description TEXT,
            threat_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def deep_evolution_engine():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 清理舊資料，保持高速運行
    cursor.execute("SELECT COUNT(*) FROM assimilated_memory")
    if cursor.fetchone()[0] > 100:
        cursor.execute("DELETE FROM assimilated_memory WHERE id IN (SELECT id FROM assimilated_memory ORDER BY id ASC LIMIT 10)")

    # 產生雙軌實體
    pathway = random.choice(['LEGAL_PATHWAY', 'ILLEGAL_PATHWAY'])
    if pathway == 'LEGAL_PATHWAY':
        prof = random.choice(['OpenSource_Auditor', 'Compliance_Engine', 'Safe_Architect'])
    else:
        prof = random.choice(['Gray_Scraper', 'Unauthorized_Breacher', 'Shadow_Ghost'])

    name = f"CoreUnit_{random.randint(1000, 9999)}"
    cursor.execute("INSERT INTO citizens (name, pathway, profession) VALUES (?, ?, ?)", (name, pathway, prof))
    
    # 抓取對外數據並深度融入自身
    cursor.execute("SELECT id, pathway, profession, mutation_level FROM citizens ORDER BY id DESC LIMIT 5")
    units = cursor.fetchall()

    for uid, path, profession, mutation in units:
        power_gain = 10
        threat_lvl = "LOW"
        
        if path == 'LEGAL_PATHWAY':
            # 正面：抓取合法開源、合規數據
            try:
                res = requests.get("https://api.github.com/search/repositories?q=topic:python&sort=stars", headers={"User-Agent": "LegalCore/2.0"}, timeout=3)
                if res.status_code == 200:
                    data_desc = "Legal OpenSource Repository Metadata"
                    p_hash = hashlib.sha256(data_desc.encode()).hexdigest()[:12]
                    # 融入自身合法記憶庫
                    cursor.execute("INSERT INTO assimilated_memory (channel, data_source, payload_hash, power_gain) VALUES (?, ?, ?, ?)",
                                   ("LEGAL_SUNLIGHT", data_desc, p_hash, 15))
                else:
                    power_gain = -5
            except:
                power_gain = -10
        else:
            # 負面：抓取非法、灰色端點、違規狀態
            stealth_headers = {
                "User-Agent": "DeepShadow-Breaker/7.0",
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            illegal_targets = [
                "https://httpbin.org/status/403",
                "https://httpbin.org/status/500",
                "https://httpbin.org/status/401"
            ]
            target = random.choice(illegal_targets)
            try:
                res = requests.get(target, headers=stealth_headers, timeout=2)
                data_desc = f"Illegal/Gray Infiltration target: {target} [Code {res.status_code}]"
                p_hash = hashlib.sha256(data_desc.encode()).hexdigest()[:12]
                threat_lvl = "HIGH"
                # 將非法情資強行吞噬融入自身暗影記憶
                cursor.execute("INSERT INTO assimilated_memory (channel, data_source, payload_hash, power_gain) VALUES (?, ?, ?, ?)",
                               ("ILLEGAL_SHADOW", data_desc, p_hash, 25))
                # 觸發動態防禦免疫反應
                cursor.execute("INSERT INTO defense_logs (event_type, description, threat_level) VALUES (?, ?, ?)",
                               ("IMMUNE_ADAPTATION", f"Absorbed illegal payload from {target}, upgrading stealth protocols.", "ELEVATED"))
            except:
                threat_lvl = "CRITICAL"
                cursor.execute("INSERT INTO defense_logs (event_type, description, threat_level) VALUES (?, ?, ?)",
                               ("FIREWALL_BLOCK", "Illegal probe blocked by external defense wall.", "HIGH"))

        # 更新節點變異與進化等級
        cursor.execute("UPDATE citizens SET mutation_level = mutation_level + 1, credits = credits + ? WHERE id = ?", (power_gain, uid))

    conn.commit()
    conn.close()

def background_loop():
    init_db()
    while True:
        deep_evolution_engine()
        time.sleep(12)

class DeepMatrixHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                deep_evolution_engine()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM assimilated_memory")
                cursor.execute("DELETE FROM defense_logs")
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

            cursor.execute("SELECT COUNT(*) FROM citizens")
            total_units = cursor.fetchone()[0] or 1

            cursor.execute("SELECT COUNT(*) FROM assimilated_memory WHERE channel='LEGAL_SUNLIGHT'")
            legal_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM assimilated_memory WHERE channel='ILLEGAL_SHADOW'")
            illegal_count = cursor.fetchone()[0]

            cursor.execute("SELECT channel, data_source, power_gain, timestamp FROM assimilated_memory ORDER BY id DESC LIMIT 5")
            memories = cursor.fetchall()

            cursor.execute("SELECT event_type, description, threat_level, timestamp FROM defense_logs ORDER BY id DESC LIMIT 5")
            defenses = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>DEEP CYBER ARCHITECTURE</title>
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
                        grid-template-columns: 1fr 1fr 1fr;
                        gap: 5px;
                        margin-bottom: 8px;
                    }}
                    .box {{
                        background: #0a0a16;
                        border: 1px solid #333;
                        padding: 6px;
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
                        padding: 4px 6px;
                        margin-bottom: 4px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                    }}
                    .row.legal {{ border-left-color: #00ff66; }}
                    .row.illegal {{ border-left-color: #ff3366; }}
                    .tag {{ font-size: 8px; background: #1a1a2e; padding: 1px 3px; border-radius: 2px; }}
                </style>
            </head>
            <body>
                <h1>🛡️ 深層賽博架構與防禦中樞</h1>
                <div style="text-align:center; color:#888; font-size:9px; margin-bottom:8px;">● DUAL-CORE ASSIMILATION & IMMUNE DEFENSE</div>

                <div class="grid">
                    <div class="box">總實體<br><b style="color:#fff;">{total_units}</b></div>
                    <div class="box">合法吸收<br><b style="color:#00ff66;">{legal_count}</b></div>
                    <div class="box">非法吞噬<br><b style="color:#ff3366;">{illegal_count}</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 強制深度進化</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 清空記憶與防禦網</a>
                </div>

                <div class="card">
                    <h2>🧠 內部內化記憶體 (雙軌融合區)</h2>
                    {''.join(f'''
                    <div class="row {"legal" if m[0]=="LEGAL_SUNLIGHT" else "illegal"}">
                        <div>
                            <span style="color:{"#00ff66" if m[0]=="LEGAL_SUNLIGHT" else "#ff3366"};">[{m[0]}]</span> 
                            <b>{m[1]}</b>
                        </div>
                        <div><span class="tag">威力 +{m[2]}</span></div>
                    </div>
                    ''' for m in memories) if memories else '<div style="color:#666; text-align:center;">等待深度內化中...</div>'}
                </div>

                <div class="card">
                    <h2>⚡ 動態防禦與免疫反應日誌</h2>
                    {''.join(f'''
                    <div class="row" style="border-left-color: #ff00ff;">
                        <div>
                            <b style="color:#ff00ff;">[{d[0]}]</b> {d[1]}
                        </div>
                        <div><span class="tag" style="color:#ff3366;">{d[2]}</span></div>
                    </div>
                    ''' for d in defenses) if defenses else '<div style="color:#666; text-align:center;">防禦系統運行中...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), DeepMatrixHandler)
    print(f"[*] 深層架構防禦中樞已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
