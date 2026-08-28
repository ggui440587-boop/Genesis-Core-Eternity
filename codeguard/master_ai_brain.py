import urllib.request
import json
import time

class MasterAIBrain:
    def __init__(self, robot_url="http://127.0.0.1:8000"):
        self.robot_url = robot_url
        print("-> ⚡ [主控大腦] 初始化完成：具備自主分析、風險評估與預測能力。")

    def evaluate_and_command(self, situational_data):
        """大腦進行對話分析、風險預測，並向機器人下達命令"""
        print(f"\n-> 🧠 [大腦思考與對話] 正在分析情境: 『{situational_data}』")

        # 大腦進行風險預測與邏輯評估
        if "未知區域" in situational_data or "敵意" in situational_data:
            risk_level = "HIGH"
            command = "CAUTIOUS_ADVANCE"
            speech = "預測前方可能存在高風險，我要求機器人採取謹慎推進並隨時準備防禦。"
        else:
            risk_level = "LOW"
            command = "STANDARD_PATROL"
            speech = "情境安全，預測無重大風險，指派機器人執行標準巡邏。"

        print(f"-> 🗣️ [大腦內心對話/分析]: {speech}")
        print(f"-> 📊 [風險評估結果]: {risk_level}")

        payload = {
            "command": command,
            "risk_level": risk_level,
            "speech_context": speech
        }

        self.transmit_to_robot(payload)

    def transmit_to_robot(self, payload):
        """將大腦指令透過網路傳遞給機器人本體"""
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.robot_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            print(f"-> 🚀 [大腦指令下達] 正在傳送命令至機器人本體...")
            with urllib.request.urlopen(req, timeout=3) as res:
                result = json.loads(res.read().decode('utf-8'))
                print(f"-> [✔] 收到機器人本體回報: {result}")
        except Exception as e:
            print(f"-> [❌] 無法連線至機器人本體: {e}")

if __name__ == "__main__":
    brain = MasterAIBrain()
    # 模擬主控大腦接收情境並進行風險評估與指揮
    brain.evaluate_and_command("前方發現未知區域且可能有敵意訊號")

