import http.server
import socketserver
import json

PORT = 7777

class AIExecutionHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            packet = json.loads(post_data.decode('utf-8'))
            ai_decision = packet.get("decision", "IDLE")
            target_action = packet.get("action", "NONE")

            print(f"\n-> 🤖 [機器人接收端] 收到來自超級電腦 AI 的決策！")
            print(f"   ├─ AI 決策理由: {ai_decision}")
            print(f"   └─ 執行實體動作: {target_action}")

            # 這裡可以接上真實的機器人硬體驅動（如馬達、機械臂）
            print(f"-> ⚙️ [物理執行] 機器人正在現實世界中執行: {target_action}...")

            response = {"status": "EXECUTED", "action": target_action}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AIExecutionHandler) as httpd:
        print(f"-> 🤖 機器人實體執行端已啟動，正在監聽連接埠 {PORT}...")
        httpd.serve_forever()

