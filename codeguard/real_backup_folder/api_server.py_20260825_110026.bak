import http.server
import socketserver
import json

# ==============================================================
# System API Server Module - 系統遠端網路通訊與 API 介面
# ==============================================================

PORT = 8080

class GenesisAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """處理來自外部的 GET 請求，回傳系統當前狀態"""
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        response_data = {
            "system": "Genesis-Core-Eternity",
            "status": "ONLINE",
            "message": "系統運作正常，遠端 API 連線通暢！"
        }
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))

def run_server():
    """啟動系統的對外網路伺服器"""
    with socketserver.TCPServer(("", PORT), GenesisAPIHandler) as httpd:
        print("=" * 60)
        print(f" 🌐 系統 API 伺服器已啟動，正在聆聽連接埠: {PORT}")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[伺服器關閉] 收到中斷訊號，對外通訊介面安全關閉。")

if __name__ == "__main__":
    run_server()

