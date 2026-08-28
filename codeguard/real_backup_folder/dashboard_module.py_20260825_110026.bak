import http.server
import socketserver
import sqlite3
import os

PORT = 8080
DB_NAME = "fusion_hub.db"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # 讀取資料庫中的最新記錄
        records_html = ""
        if os.path.exists(DB_NAME):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, url, timestamp FROM projects ORDER BY id DESC LIMIT 5")
                rows = cursor.fetchall()
                conn.close()

                for row in rows:
                    records_html += f"<li><b>ID:</b> {row[0]} | <b>標題:</b> {row[1]} | <b>時間:</b> {row[3]}</li>"
            except Exception as e:
                records_html = f"<li>讀取資料庫發生錯誤: {e}</li>"
        else:
            records_html = "<li>尚未建立資料庫記錄。</li>"

        # 組合網頁內容
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Genesis-Core-Eternity 儀表板</title>
            <style>
                body {{ font-family: sans-serif; background: #121212; color: #e0e0e0; padding: 20px; }}
                h1 {{ color: #00ff66; }}
                ul {{ background: #1e1e1e; padding: 15px; border-radius: 8px; }}
                li {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <h1>🚀 Genesis 專案狀態儀表板</h1>
            <p>當前多語言生態系運作正常，以下為最新的資料庫專案記錄：</p>
            <ul>
                {records_html}
            </ul>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"-> 🌐 [Dashboard] 本機網頁儀表板已啟動！請在瀏覽器造訪: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n-> [!] 網頁儀表板已關閉。")

