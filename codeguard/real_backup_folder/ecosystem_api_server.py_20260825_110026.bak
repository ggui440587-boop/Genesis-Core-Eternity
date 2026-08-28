from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# ==============================================================
# Ecosystem API Server - 跨語言通訊與狀態查詢 API 伺服器
# ==============================================================

class EcosystemAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """處理來自其他語言或前端的 GET 請求"""
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()

            response_data = {
                "status": "ONLINE",
                "project": "Genesis-Core-Eternity",
                "message": "跨語言 API 伺服器運作正常！"
            }
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        # 覆寫並簡化預設的日誌輸出格式
        print(f"🌐 [API 請求] 收到來自客戶端的連線: {args[0]}")

def run_server(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, EcosystemAPIHandler)
    print("=" * 60)
    print(f" 🚀 [API 啟動] Genesis-Core-Eternity 跨語言伺服器已啟動！")
    print(f" 聆聽連接埠: http://localhost:{port}/status")
    print(f" 提示: 在 Termux 中若要停止伺服器，請按下 [Ctrl + C]")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 [API 關閉] 伺服器已安全停止。")

if __name__ == "__main__":
    run_server()

