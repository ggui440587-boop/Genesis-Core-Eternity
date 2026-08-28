import http.server
import socketserver
import json

PORT = 6666

class RobotBodyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            packet = json.loads(post_data.decode('utf-8'))
            brain_mood = packet.get("mood", "NEUTRAL")
            brain_dialogue = packet.get("dialogue", "...")
            physical_action = packet.get("action", "IDLE")

            print(f"\n-> 🤖 [機器人身體接收] 收到大腦的訊號！")
            print(f"   ├─ 大腦心情: {brain_mood}")
            print(f"   ├─ 大腦對話/打字: 『{brain_dialogue}』")
            print(f"   └─ 執行實體動作: {physical_action}")

            # 模擬機器人執行實體操作
            print(f"-> ⚙️ [物理執行中] 正在配合大腦的心情與指令完成動作...\n")

            response = {"status": "BODY_EXECUTED", "action": physical_action}
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

