import http.server
import socketserver
import json

PORT = 9000

class RobotAgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            packet = json.loads(post_data.decode('utf-8'))
            task_id = packet.get("task_id", "UNKNOWN")
            command = packet.get("command", "IDLE")
            priority = packet.get("priority", 1)

            print(f"\n-> 🤖 [機器人節點] 收到中央 AI 指令！")
            print(f"   ├─ 任務編號: {task_id}")
            print(f"   ├─ 執行指令: {command}")
            print(f"   └─ 任務優先級: {priority}")

            # 模擬機器人執行實體操作
            print(f"-> ⚙️ [執行中] 正在現實世界中完成動作: {command}...")

            response = {"status": "SUCCESS", "task_id": task_id, "executed_command": command}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), RobotAgentHandler) as httpd:
        print(f"-> 🤖 機器人節點代理已啟動，正在監聽連接埠 {PORT}...")
        httpd.serve_forever()

