import http.server
import socketserver
import json
import random

PORT = 8000

class RobotAutonomousHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            packet = json.loads(post_data.decode('utf-8'))
            brain_command = packet.get("command", "IDLE")
            risk_assessment = packet.get("risk_level", "LOW")

            print(f"\n-> 🤖 [機器人本體] 收到大腦指令！")
            print(f"   ├─ 大腦下達指令: {brain_command}")
            print(f"   └─ 大腦風險評估: {risk_assessment}")

            # 機器人本體在執行當下進行自主判斷
            print(f"-> ⚙️ [機器人自主判斷中] 掃描現場實體環境...")
            local_obstacle_detected = random.choice([True, False])

            if local_obstacle_detected and risk_assessment == "HIGH":
                local_action = "LOCAL_EMERGENCY_EVASION"
                print(f"   ⚠️ [自主反應] 偵測到即時危險！機器人自主決定執行緊急閃避，覆寫部分大腦指令。")
            else:
                local_action = f"EXECUTE_{brain_command}_SUCCESS"
                print(f"   ✔ [自主反應] 環境安全，順利完成大腦交辦的實體操作。")

            response = {
                "status": "COMPLETED",
                "local_action_taken": local_action,
                "obstacle_status": local_obstacle_detected
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), RobotAutonomousHandler) as httpd:
        print(f"-> 🤖 機器人本體端已啟動，正在監聽連接埠 {PORT}...")
        httpd.serve_forever()

