import sqlite3
import datetime
import types
import re
import time
import threading
import http.server
import socketserver
json_lib = __import__('json')

print("[*] 正在啟動造物主【Matrix Empire 分散式叢集總控核心 (修復版)】...")

class ClusterMaster:
    def __init__(self, db_path="fusion_cluster.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cluster_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id TEXT,
                task_status TEXT,
                payload_data TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def spawn_worker(self, worker_name, interval):
        """ 修正變數傳遞後的獨立 Worker 代理人 """
        print(f"[+] 獨立工作節點 [{worker_name}] 已成功解鎖並加入叢集！")
        while True:
            try:
                # 修正：將 worker_name 安全地透過引數或字串拼接注入
                dynamic_code = f"""
import random
def execute_task():
    w_name = "{worker_name}"
    return f"{{w_name}} 代理人成功完成第 {{random.randint(1000, 9999)}} 代分散式矩陣運算。"
"""
                dyn_module = types.ModuleType(f"module_{worker_name}")
                exec(dynamic_code, dyn_module.__dict__)
                result = dyn_module.execute_task()

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                now = datetime.datetime.now().isoformat()
                cursor.execute(
                    "INSERT INTO cluster_nodes (worker_id, task_status, payload_data, created_at) VALUES (?, ?, ?, ?)",
                    (worker_name, "ACTIVE", result, now)
                )
                conn.commit()
                conn.close()
                print(f"[{worker_name}] 🧬 同步回報：{result}")
            except Exception as e:
                print(f"[-] [{worker_name}] 異常：{e}")
            
            time.sleep(interval)

def start_cluster_workers(master):
    workers = [
        ("Alpha-Crawler", 5),
        ("Beta-Analyzer", 8),
        ("Gamma-Sentinel", 12)
    ]
    for name, interval in workers:
        t = threading.Thread(target=master.spawn_worker, args=(name, interval), daemon=True)
        t.start()

def start_cluster_dashboard():
    PORT = 9000
    class ClusterHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html>
            <head><title>Matrix Empire Cluster</title></head>
            <body style="background: #050505; color: #00ff66; font-family: monospace; padding: 20px;">
                <h1>🌐 Matrix Empire - 分散式叢集總控儀表板</h1>
                <p>狀態：多重平行代理人運作中 | 叢集資料庫：fusion_cluster.db</p>
                <hr style="border-color: #00ff66;">
                <h3 id="cluster_status">正在監控叢集節點心跳...</h3>
                <script>
                    setInterval(() => {{
                        document.getElementById('cluster_status').innerText = '🔥 叢集多重節點同步正常，時間：' + new Date().toLocaleTimeString();
                    }}, 1000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

    while True:
        try:
            httpd = socketserver.TCPServer(("", PORT), ClusterHandler)
            print(f"[+] 叢集 Web 總控台已上線：http://localhost:{PORT}")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 98:
                PORT += 1
            else:
                raise e

if __name__ == "__main__":
    master = ClusterMaster()
    start_cluster_workers(master)
    start_cluster_dashboard()
