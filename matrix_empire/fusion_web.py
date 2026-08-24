import http.server
import socketserver
import sqlite3
import json

PORT = 8080

class EvolutionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/targets":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            conn = sqlite3.connect("fusion_hub.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content, category, created_at FROM evolution_targets ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            
            data = []
            for r in rows:
                data.append({
                    "id": r[0],
                    "title": r[1],
                    "content": r[2],
                    "category": r[3],
                    "created_at": r[4]
                })
            
            self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <head><title>Matrix Empire Dashboard</title></head>
            <body style="background: #111; color: #0f0; font-family: monospace; padding: 20px;">
                <h2>🧬 Matrix Empire - 動態演化監控面板</h2>
                <p>正在監控 fusion_hub.db 中的自我演化獵物...</p>
                <hr style="border-color: #0f0;">
                <pre id="data" style="white-space: pre-wrap;">載入中...</pre>
                <script>
                    fetch('/api/targets')
                        .then(res => res.json())
                        .then(data => {
                            document.getElementById('data').innerText = JSON.stringify(data, null, 2);
                        });
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

print(f"[*] 正在啟動造物主 Web 儀表板，通訊埠：{PORT}...")
with socketserver.TCPServer(("", PORT), EvolutionHandler) as httpd:
    print(f"[+] 伺服器已上線！請在瀏覽器打開 http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] 儀表板已安全關閉。")
