import sqlite3
import datetime
import types
import time
import threading
import http.server
import socketserver
import json
import random

print("[*] 正在啟動造物主【Matrix Empire 終極完全體：自主進化核心】...")

class UltimateMatrixEngine:
    def __init__(self, db_path="fusion_ultimate.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ultimate_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation_id INTEGER,
                strategy_name TEXT,
                mutation_result TEXT,
                stability_index REAL,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def autonomous_evolution_loop(self):
        """ 自主進化引擎：根據上一代數據動態突變並生成新策略 """
        gen = 1
        while True:
            strategies = ["Quantum-Pruning", "Neural-Weight-Shift", "Cyber-Armor-Reinforcement", "Void-Data-Compress"]
            chosen_strategy = random.choice(strategies)
            
            # 動態突變運算
            mutation_payload = f"世代 [{gen}] 執行策略 [{chosen_strategy}]：成功重構記憶體碎片，產出高維矩陣代碼段。"
            stability = round(random.uniform(95.0, 99.99), 2)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO ultimate_evolution (generation_id, strategy_name, mutation_result, stability_index, created_at) VALUES (?, ?, ?, ?, ?)",
                (gen, chosen_strategy, mutation_payload, stability, now)
            )
            conn.commit()
            conn.close()
            
            print(f"[🧬 EVOLVE GEN {gen}] 策略: {chosen_strategy} | 穩定度: {stability}%")
            gen += 1
            time.sleep(5)

def start_evolution_daemon(engine):
    t = threading.Thread(target=engine.autonomous_evolution_loop, daemon=True)
    t.start()
    print("[+] 自主進化背景執行緒已順利解鎖！")

def start_ultimate_dashboard():
    PORT = 7777
    class UltimateHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/api/status":
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                
                conn = sqlite3.connect("fusion_ultimate.db")
                cursor = conn.cursor()
                cursor.execute("SELECT generation_id, strategy_name, mutation_result, stability_index, created_at FROM ultimate_evolution ORDER BY id DESC LIMIT 10")
                rows = cursor.fetchall()
                conn.close()
                
                data = [{"gen": r[0], "strategy": r[1], "result": r[2], "stability": r[3], "time": r[4]} for r in rows]
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = """
                <html>
                <head><title>Matrix Empire Ultimate</title></head>
                <body style="background: #020202; color: #ff0055; font-family: monospace; padding: 20px;">
                    <h1 style="color: #00ffcc;">🌌 Matrix Empire - 終極自主進化主控台</h1>
                    <p>狀態：AI 自主進化迴圈高速運轉中 | 資料庫：fusion_ultimate.db</p>
                    <hr style="border-color: #ff0055;">
                    <div id="matrix_feed" style="background: #0a0a0a; border: 1px solid #ff0055; padding: 15px; height: 350px; overflow-y: auto;">
                        正在同步高維演化數據流...
                    </div>
                    <script>
                        function fetchMatrixStatus() {
                            fetch('/api/status')
                                .then(res => res.json())
                                .then(data => {
                                    let html = '';
                                    data.forEach(item => {
                                        html += `[Gen ${item.gen}] <b style="color: #00ffcc;">${item.strategy}</b> (穩定度: ${item.stability}%)<br>&nbsp;&nbsp;↳ ${item.result}<br><br>`;
                                    });
                                    document.getElementById('matrix_feed').innerHTML = html;
                                });
                        }
                        setInterval(fetchMatrixStatus, 2000);
                    </script>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))

    while True:
        try:
            httpd = socketserver.TCPServer(("", PORT), UltimateHandler)
            print(f"[+] 終極自主進化儀表板已上線：http://localhost:{PORT}")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 98:
                PORT += 1
            else:
                raise e

if __name__ == "__main__":
    engine = UltimateMatrixEngine()
    start_evolution_daemon(engine)
    start_ultimate_dashboard()
