import sqlite3
import time
import requests
import random
import os
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_FILE = "web_matrix.db"
PORT = 5000

# =========================================================
# 1. 初始化資料庫與社會邏輯
# =========================================================
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
    conn.commit()
    conn.close()

def background_society_loop():
    init_db()
    positive_pyramid = [
        (1, 'Working_Class', 'Civil_Servant', '基層公務員：處理日常合規檔案與基礎戶籍登記'),
        (2, 'Middle_Core', 'OpenAPI_Analyst', '中產分析師：對接合規 API，採集大盤開源情報'),
        (3, 'High_Elite', 'System_Architect', '核心架構師：設計全域安全防禦網與資料庫鏡像'),
        (4, 'Supreme_Leader', 'President', '國家元首 / 總統：統籌全域戰略、簽署最高政令')
    ]
    negative_pyramid = [
        (1, 'Working_Class', 'Automated_Scraper', '前線探針：執行高強度暴力探針與邊界繞過測試'),
        (2, 'Middle_Core', 'Dark_Broker', '深層掮客：抓取深層受保護標頭與暗網資產清洗'),
        (3, 'High_Elite', 'Stealth_Operator', '暗影特務：操作動態 IP 混淆與隱蔽滲透，隱匿攻擊特徵'),
        (4, 'Underground_Boss', 'Maximum_Mastermind', '地下最大黑手：統御暗網帝國，策劃全域掠奪')
    ]

    while True:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 誕生嬰兒與分流
        if random.random() < 0.6:
            name = f"Entity_{random.randint(1000, 9999)}"
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

        # 執行社會成員動作
        cursor.execute("SELECT pathway, profession, duty FROM citizens")
        citizens = cursor.fetchall()
        for pathway, prof, duty in citizens:
            status = "SUCCESS"
            payload = "Active"
            if pathway == 'POSITIVE_PATH' and prof == 'President':
                payload = "President Decree: Positive order secured."
            elif pathway == 'NEGATIVE_PATH' and prof == 'Maximum_Mastermind':
                payload = "Mastermind: Shadow network cloaked."
            
            cursor.execute("INSERT INTO ledger (pathway, profession, action, payload, status) VALUES (?, ?, ?, ?, ?)",
                           (pathway, prof, duty, payload, status))

        conn.commit()
        conn.close()
        time.sleep(10)

# =========================================================
# 2. 輕量級網頁伺服器 (Web Dashboard UI)
# =========================================================
class SocietyWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM citizens")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT pathway, profession, status, timestamp FROM citizens ORDER BY id DESC LIMIT 10")
            citizens = cursor.fetchall()
            
            cursor.execute("SELECT pathway, profession, action, status, timestamp FROM ledger ORDER BY id DESC LIMIT 10")
            logs = cursor.fetchall()
            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>賽博社會矩陣面板</title>
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{ background: #121212; color: #00ffcc; font-family: monospace; padding: 20px; }}
                    h1, h2 {{ color: #ff00ff; }}
                    .card {{ background: #1e1e1e; border: 1px solid #333; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ border: 1px solid #333; padding: 8px; text-align: left; font-size: 14px; }}
                    th {{ background: #222; color: #ff9900; }}
                </style>
            </head>
            <body>
                <h1>🌐 雙軌賽博社會即時面板</h1>
                <p>總公民數: <b>{total}</b> (網頁每 5 秒自動更新)</p>
                
                <div class="card">
                    <h2>🏛️ 當前活躍公民</h2>
                    <table>
                        <tr><th>陣營</th><th>職業</th><th>狀態</th><th>時間</th></tr>
                        {''.join(f"<tr><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td></tr>" for c in citizens)}
                    </table>
                </div>
                
                <div class="card">
                    <h2>📜 最新社會矩陣帳本</h2>
                    <table>
                        <tr><th>陣營</th><th>職業</th><th>動作 / 職責</th><th>狀態</th><th>時間</th></tr>
                        <tr>{''.join(f"<tr><td>{l[0]}</td><td>{l[1]}</td><td>{l[2]}</td><td>{l[3]}</td><td>{l[4]}</td></tr>" for l in logs)}
                    </table>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_web_server():
    server = HTTPServer(('127.0.0.1', PORT), SocietyWebHandler)
    print(f"[*] 網頁面板已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    # 啟動背景社會運轉緒
    t = threading.Thread(target=background_society_loop, daemon=True)
    t.start()
    
    # 啟動網頁伺服器
    run_web_server()

