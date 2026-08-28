import http.server
import socketserver
import threading
import urllib.request
import json
import time

PORT = 8099

# 1. 定義一個簡單的本機 HTTP 伺服器處理常式
class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"\n-> 📡 [真實網路接收] 伺服器成功收到來自客戶端的 HTTP 請求！")
        response_data = {"status": "CONNECTED", "message": "真實網路連接成功"}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def log_message(self, format, *args):
        # 覆寫以保持終端機輸出乾淨
        return

def run_server():
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"-> 🌐 [伺服器啟動] 正在本機連接埠 {PORT} 監聽真實網路流量...")
        httpd.handle_request() # 處理一次請求後自動關閉

if __name__ == "__main__":
    # 2. 在背景執行緒中啟動伺服器
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1) # 確保伺服器就緒

    # 3. 發起真實的網路 HTTP 請求
    target_url = f"http://127.0.0.1:{PORT}"
    print(f"-> 🚀 [客戶端發起] 正在透過真實網路通道向 {target_url} 發送請求...")

    try:
        with urllib.request.urlopen(target_url, timeout=3) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"-> [✔] 收到伺服器回應: {result}")
            print(f"-> 🎉 結論：這在軟體世界中是百分之百真實且實際運作的網路連接！")
    except Exception as e:
        print(f"-> [❌] 連接失敗: {e}")

