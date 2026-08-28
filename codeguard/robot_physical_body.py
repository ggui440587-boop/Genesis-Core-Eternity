import http.server
import socketserver
import json

PORT = 8899

class RobotBodyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            packet = json.loads(post_data.decode('utf-8'))
            brain_mood = packet.get("mood", "CALM")
            brain_speech = packet.get("speech", "...")
            physical_action = packet.get("action", "IDLE")
            speed = packet.get("speed", 0)

            print(f"\n-> 🤖 [機器人身體接收] 收到大腦核心指令！")
            print(f"   ├─ 大腦心情狀態: {brain_mood}")
            print(f"   ├─ 大腦語音/說話: 『{brain_speech}』")
            print(f"   └─ 執行實體動作: {physical_action} (速度: {speed})")

            # 模擬硬體層面的實體移動與操作
            print(f"-> ⚙️ [物理執行中] 機器人正在現實中執行 {physical_action}...\n")

            response = {"status": "SUCCESS", "executed": physical_action}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), RobotBodyHandler) as httpd:
        print(f"-> 🤖 機器人身體端已啟動，正在監聽連接埠 {PORT}...")
        httpd.serve_forever()

