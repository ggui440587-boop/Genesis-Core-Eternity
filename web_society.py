import sqlite3
import time
import requests
import random
import os
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "web_matrix.db"
PORT = 5050

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            pathway TEXT,
            tier INT,
            social_class TEXT,
            profession TEXT,
            duty TEXT,
            credits INTEGER DEFAULT 100,
            health INTEGER DEFAULT 100,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pathway TEXT,
            profession TEXT,
            action TEXT,
            payload TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 內化記憶庫：融合合法與非法的所有外部抓取成果
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assimilated_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            content TEXT,
            power_boost INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def execute_society_cycle():
    init_db()
    positive_pyramid = [
        (1, 'Working_Class', 'Civic_Agent', '合法公務：登記授權公開紀錄'),
        (2, 'Middle_Core', 'OpenSource_Analyst', '合規分析：抓取合法開源專案與授權代碼'),
        (3, 'High_Elite', 'Legal_Architect', '架構師：建立合規防禦知識庫'),
        (4, 'Supreme_Leader', 'Prime_Minister', '領袖：統籌陽光社會全面進化')
    ]
    negative_pyramid = [
        (1, 'Working_Class', 'Underground_Probe', '暗影探針：強行探測未授權或違規端點'),
        (2, 'Middle_Core', 'Shadow_Scraper', '地下掮客：擷取非法與灰色地帶數據'),
        (3, 'High_Elite', 'Ghost_Operator', '黑帽特務：繞過防禦並吞噬違規標頭'),
        (4, 'Underground_Boss', 'Syndicate_Master', '地下黑手：統御所有非法情報與暗網記憶')
    ]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 清理舊歷史，維持輕量
    cursor.execute("DELETE FROM ledger WHERE id NOT IN (SELECT id FROM ledger ORDER BY id DESC LIMIT 50)")

    # 催生新節點
    name = f"Node_{random.randint(1000, 9999)}"
    chosen_line = random.choice(['POSITIVE_PATH', 'NEGATIVE_PATH'])
    tier_idx = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.15, 0.05], k=1)[0]
    
    if chosen_line == 'POSITIVE_PATH':
        tier, s_class, prof, duty = positive_pyramid[tier_idx]
    else:
        tier, s_class, prof, duty = negative_pyramid[tier_idx]
        
    cursor.execute('''
        INSERT INTO citizens (name, pathway, tier, social_class, profession, duty, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, chosen_line, tier, s_class, prof, duty, "運行中"))

    # 執行抓取與內化
    cursor.execute("SELECT id, pathway, profession, credits, health FROM citizens ORDER BY id DESC LIMIT 6")
    citizens = cursor.fetchall()
    
    for cid, pathway, prof, credits, health in citizens:
        status = "SUCCESS"
        payload = "Active"
        score_delta = 15
        health_delta = 0
        
        # --- 正面線：絕對合法、合規、公開的資料抓取並融入自身 ---
        if pathway == 'POSITIVE_PATH':
            if prof == 'Civic_Agent':
                payload = "Authorized public record verified."
            elif prof == 'OpenSource_Analyst':
                try:
                    res = requests.get("https://api.github.com/search/repositories?q=topic:python&sort=stars", headers={"User-Agent": "LegalOpenSource/1.0"}, timeout=3)
                    if res.status_code == 200:
                        items = res.json().get('items', [])
                        top_repo = items[random.randint(0, min(4, len(items)-1))]['name'] if items else 'Python-Safe'
                        payload = f"Absorbed Legal Repo: {top_repo}"
                        # 融入自身合法知識庫
                        cursor.execute("INSERT INTO assimilated_memory (source_type, content, power_boost) VALUES (?, ?, ?)", 
                                       ("LEGAL_KNOWLEDGE", f"OpenSource Repo: {top_repo}", 10))
                    else:
                        payload = "GitHub Rate Limited"
                except:
                    status = "TIMEOUT"
                    score_delta = -15
                    health_delta = -10
            elif prof == 'Legal_Architect':
                payload = "Legal defense database updated."
            elif prof == 'Prime_Minister':
                payload = "Authorized societal growth integrated."

        # --- 負面線：非法、灰色地帶、未授權與異常漏洞的抓取並融入自身 ---
        elif pathway == 'NEGATIVE_PATH':
            stealth_headers = {
                "User-Agent": "UndergroundReaper/9.0",
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            # 模擬灰色/非法探測與違規端點回應
            illegal_targets = [
                "https://httpbin.org/status/403", 
                "https://httpbin.org/status/401", 
                "https://httpbin.org/status/500",
                "https://httpbin.org/delay/1"
            ]
            chosen_target = random.choice(illegal_targets)
            
            try:
                res = requests.get(chosen_target, headers=stealth_headers, timeout=2)
                payload = f"Breached Illegal/Gray Target [{res.status_code}]"
                # 將非法/灰色數據強行融入自身暗影記憶庫
                cursor.execute("INSERT INTO assimilated_memory (source_type, content, power_boost) VALUES (?, ?, ?)", 
                               ("ILLEGAL_SHADOW", f"Gray/Unauth Breach Status {res.status_code}", 20))
            except:
                status = "BLOCKED"
                score_delta = -20
                health_delta = -15
                payload = "Target lockdown resisted infiltration."

        # 更新積分與生命值
        new_credits = max(0, credits + score_delta)
        new_health = health + health_delta
        
        if new_health <= 0:
            cursor.execute("DELETE FROM citizens WHERE id = ?", (cid,))
        else:
            cursor.execute("UPDATE citizens SET credits = ?, health = ? WHERE id = ?", (new_credits, new_health, cid))

        # 寫入帳本
        cursor.execute("INSERT INTO ledger (pathway, profession, action, payload, status) VALUES (?, ?, ?, ?, ?)",
                       (pathway, prof, duty, payload, status))

    conn.commit()
    conn.close()

def background_society_loop():
    init_db()
    while True:
        execute_society_cycle()
        time.sleep(10)

class CyberSocietyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == '/action':
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'spawn':
                execute_society_cycle()
            elif cmd == 'clear_ledger':
                cursor.execute("DELETE FROM ledger")
                cursor.execute("DELETE FROM assimilated_memory")
                conn.commit()
            conn.close()
            
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM citizens")
            total = cursor.fetchone()[0] or 1
            
            cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway='POSITIVE_PATH'")
            pos_total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway='NEGATIVE_PATH'")
            neg_total = cursor.fetchone()[0]
            
            pos_pct = int((pos_total / total) * 100) if total > 0 else 50
            neg_pct = 100 - pos_pct
            
            cursor.execute("SELECT name, pathway, profession, credits, health FROM citizens ORDER BY id DESC LIMIT 5")
            citizens = cursor.fetchall()
            
            cursor.execute("SELECT source_type, content, power_boost, timestamp FROM assimilated_memory ORDER BY id DESC LIMIT 5")
            memories = cursor.fetchall()
            
            cursor.execute("SELECT pathway, profession, action, status, timestamp FROM ledger ORDER BY id DESC LIMIT 5")
            logs = cursor.fetchall()
            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>LEGAL & ILLEGAL ASSIMILATED MATRIX</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="refresh" content="5">
                <style>
                    * {{ box-sizing: border-box; }}
                    body {{
                        background-color: #030307;
                        color: #00ffcc;
                        font-family: monospace;
                        padding: 10px;
                        margin: 0;
                        font-size: 13px;
                    }}
                    h1 {{
                        color: #ff00ff;
                        text-align: center;
                        text-shadow: 0 0 8px #ff00ff;
                        font-size: 15px;
                        margin: 5px 0;
                    }}
                    .subtitle {{
                        text-align: center;
                        color: #00ffcc;
                        font-size: 10px;
                        margin-bottom: 10px;
                    }}
                    .stats-grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr 1fr;
                        gap: 6px;
                        margin-bottom: 8px;
                    }}
                    .stat-card {{
                        background: #0d0d1a;
                        border: 1px solid #333;
                        padding: 6px;
                        text-align: center;
                        border-radius: 4px;
                    }}
                    .bar-container {{
                        background: #111;
                        height: 8px;
                        border-radius: 4px;
                        display: flex;
                        overflow: hidden;
                        margin-bottom: 10px;
                        border: 1px solid #333;
                    }}
                    .bar-pos {{ background: #00ff66; width: {pos_pct}%; }}
                    .bar-neg {{ background: #ff3366; width: {neg_pct}%; }}

                    .control-panel {{
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
                        border-radius: 4px;
                        text-align: center;
                        text-decoration: none;
                        font-weight: bold;
                        font-size: 11px;
                    }}
                    .btn-danger {{ border-color: #ff3366; color: #ff3366; }}
                    .card {{
                        background: #090913;
                        border: 1px solid #222244;
                        padding: 8px;
                        margin-bottom: 8px;
                        border-radius: 4px;
                    }}
                    h2 {{
                        color: #ff9900;
                        font-size: 11px;
                        border-bottom: 1px dashed #333;
                        padding-bottom: 3px;
                        margin: 0 0 6px 0;
                    }}
                    .item-row {{
                        background: #0e0e1c;
                        border-left: 3px solid #444;
                        padding: 5px 6px;
                        margin-bottom: 5px;
                        border-radius: 2px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .item-row.pos {{ border-left-color: #00ff66; }}
                    .item-row.neg {{ border-left-color: #ff3366; }}
                    .tag {{ font-size: 9px; padding: 1px 3px; border-radius: 2px; background: #1a1a2e; }}
                </style>
            </head>
            <body>
                <h1>🌐 合法與非法情報內化矩陣</h1>
                <div class="subtitle">● LEGAL & ILLEGAL DUAL ASSIMILATION</div>
                
                <div class="stats-grid">
                    <div class="stat-card">總節點<br><b style="color:#fff;">{total}</b></div>
                    <div class="stat-card">合法光明<br><b style="color:#00ff66;">{pos_total}</b></div>
                    <div class="stat-card">非法暗影<br><b style="color:#ff3366;">{neg_total}</b></div>
                </div>

                <div class="bar-container">
                    <div class="bar-pos"></div>
                    <div class="bar-neg"></div>
                </div>

                <div class="control-panel">
                    <a class="btn" href="/action?cmd=spawn">⚡ 投遞新節點</a>
                    <a class="btn btn-danger" href="/action?cmd=clear_ledger">🗑️ 清空記憶與帳本</a>
                </div>
                
                <div class="card">
                    <h2>🧠 內部內化記憶庫 (已融合的合法/非法情資)</h2>
                    {''.join(f'''
                    <div class="item-row {"pos" if m[0]=="LEGAL_KNOWLEDGE" else "neg"}">
                        <div>
                            <span style="color:{"#00ff66" if m[0]=="LEGAL_KNOWLEDGE" else "#ff3366"};">[{m[0]}]</span> 
                            <b>{m[1]}</b>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag">進化值: +{m[2]}</span>
                        </div>
                    </div>
                    ''' for m in memories) if memories else '<div style="color:#666; font-size:10px; text-align:center;">等待雙軌吸收中...</div>'}
                </div>

                <div class="card">
                    <h2>🏛️ 雙軌公民生存狀態</h2>
                    {''.join(f'''
                    <div class="item-row {"pos" if c[1]=="POSITIVE_PATH" else "neg"}">
                        <div>
                            <span style="color:{"#00ff66" if c[1]=="POSITIVE_PATH" else "#ff3366"};">{"[正]" if c[1]=="POSITIVE_PATH" else "[負]"}</span> 
                            <b>{c[0]}</b> ({c[2]})
                        </div>
                        <div style="text-align:right;">
                            <span class="tag">積分: {c[3]}</span> 
                            <span class="tag" style="color:{"#00ff66" if c[4]>50 else "#ff3366"};">HP: {c[4]}</span>
                        </div>
                    </div>
                    ''' for c in citizens)}
                </div>
                
                <div class="card">
                    <h2>📜 雙軌抓取與內化戰報</h2>
                    {''.join(f'''
                    <div class="item-row {"pos" if l[0]=="POSITIVE_PATH" else "neg"}">
                        <div>
                            <b style="color:{"#00ff66" if l[0]=="POSITIVE_PATH" else "#ff3366"};">{l[1]}</b><br>
                            <span style="color:#aaa;">{l[2]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag" style="color:{"#00ff66" if l[3]=="SUCCESS" else "#ff3366"};">{l[3]}</span><br>
                            <span style="font-size:8px; color:#666;">{l[4][11:]}</span>
                        </div>
                    </div>
                    ''' for l in logs)}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_web_server():
    server = HTTPServer(('127.0.0.1', PORT), CyberSocietyHandler)
    print(f"[*] 雙軌內化矩陣面板已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_society_loop, daemon=True)
    t.start()
    run_web_server()
