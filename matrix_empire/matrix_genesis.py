import sqlite3
import datetime
import types
import re
import time
import threading
import http.server
import socketserver
import socket
json_lib = __import__('json')

print("[*] 正在啟動造物主【Matrix Empire 永生主控核心 (自動尋址版)】...")

class GenesisCore:
    def __init__(self, db_path="fusion_hub.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genesis_matrix (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_type TEXT,
                target_source TEXT,
                payload_title TEXT,
                payload_content TEXT,
                status TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def pulse_loop(self):
        counter = 1
        while True:
            print(f"\n[Matrix Pulse #{counter}] 脈搏跳動：正在進行新一輪矩陣自我演化...")
            
            dynamic_code = """
import re
def parse_target(html):
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    title = title_match.group(1) if title_match else "矩陣未知節點"
    return {
        "title": f"【第 {__import__('random').randint(100,999)} 代演化】" + title.strip(),
        "content": "自動化背景守護行程成功捕獲並清洗多維流動數據。"
    }
"""
            status, title, content = "SUCCESS", "", ""
            try:
                dyn_module = types.ModuleType("genesis_node")
                exec(dynamic_code, dyn_module.__dict__)
                result = dyn_module.parse_target("<html><head><title>Termux Matrix Node</title></head><body>Active</body></html>")
                title, content = result["title"], result["content"]
            except Exception as e:
                status, title, content = "FAILED", "演化例外", str(e)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO genesis_matrix (node_type, target_source, payload_title, payload_content, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                ("Daemon-Pulse", "Local-Sandbox", title, content, status, now)
            )
            conn.commit()
            conn.close()
            
            print(f"[+] 🧬 脈搏演化寫入成功：{title}")
            counter += 1
            time.sleep(10)

def start_background_daemon(core):
    t = threading.Thread(target=core.pulse_loop, daemon=True)
    t.start()
    print("[+] 背景永生脈搏線程已成功掛載！")

def start_web_dashboard():
    port = 8080
    class GenesisHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html>
            <head><title>Genesis Core Eternity</title></head>
            <body style="background: #000; color: #0f0; font-family: monospace; padding: 20px;">
                <h1>🌌 Matrix Empire - 永生主控核心儀表板 (Port: {port})</h1>
                <p>狀態：背景守護脈搏運行中 | 資料庫：fusion_hub.db</p>
                <hr style="border-color: #0f0;">
                <h3 id="status">正在同步矩陣數據...</h3>
                <script>
                    setInterval(() => {{
                        document.getElementById('status').innerText = '🔥 矩陣運轉正常，時間：' + new Date().toLocaleTimeString();
                    }}, 1000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

    # 自動尋址邏輯：如果被佔用，就自動換下一個 Port
    while True:
        try:
            httpd = socketserver.TCPServer(("", port), GenesisHandler)
            print(f"[+] 帝國 Web 儀表板已上線，成功綁定通訊埠：http://localhost:{port}")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 98: # Address already in use
                print(f"[-] 警告：通訊埠 {port} 被舊的矩陣殘骸佔用，自動切換至 {port + 1}...")
                port += 1
            else:
                raise e

if __name__ == "__main__":
    core = GenesisCore()
    start_background_daemon(core)
    start_web_dashboard()
