import urllib.request
import json
import time

class AIBrainCore:
    def __init__(self, body_url="http://127.0.0.1:6666"):
        self.body_url = body_url
        self.current_mood = "CALM"
        print("-> ⚡ [AI 大腦核心] 已啟動，具備對話、心情與思考能力。")

    def think_and_speak(self, input_situation):
        """大腦進行思考、調整心情、產生對話，並驅動機器人身體"""
        print(f"\n-> 🧠 [大腦思考中] 接收外部情境: 『{input_situation}』")

        # 根據情境改變心情與對話內容
        if "危險" in input_situation or "障礙" in input_situation:
            self.current_mood = "ALERT / 緊張"
            dialogue = "警告！偵測到前方阻礙，身體準備進行閃避或搬運作業！"
            action = "BYPASS_AND_LIFT"
        else:
            self.current_mood = "STABLE / 平靜"
            dialogue = "系統運作正常，目前環境安全，執行日常巡邏。"
            action = "PATROL_FORWARD"

        print(f"-> 💬 [大腦對話/打字]: {dialogue}")
        print(f"-> 🎭 [當前心情]: {self.current_mood}")

        payload = {
            "mood": self.current_mood,
            "dialogue": dialogue,
            "action": action
        }

        self.send_to_body(payload)

    def send_to_body(self, payload):
        """將大腦的意志傳送給機器人身體執行"""
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.body_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            print(f"-> 🚀 [傳送意志] 正在將大腦指令同步給機器人身體...")
            with urllib.request.urlopen(req, timeout=3) as res:
                result = json.loads(res.read().decode('utf-8'))
                print(f"-> [✔] 身體回報: {result}")
        except Exception as e:
            print(f"-> [❌] 無法連線至機器人身體: {e}")

if __name__ == "__main__":
    brain = AIBrainCore()
    # 模擬 AI 大腦接收到情境並產生對話與心情
    brain.think_and_speak("前方發現障礙物需要處理")

