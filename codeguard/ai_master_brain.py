import urllib.request
import json
import time

class AIMasterBrain:
    def __init__(self, body_url="http://127.0.0.1:8899"):
        self.body_url = body_url
        self.current_mood = "curious / 好奇"
        print("-> ⚡ [AI 大腦核心] 初始化完成：具備感知、情緒與真人對話能力。")

    def perceive_and_decide(self, sensory_input):
        """模擬大腦接收視覺/聽覺等感官資料後進行自主思考"""
        print(f"\n-> 🧠 [大腦感知中] 接收外部環境刺激: 『{sensory_input}』")

        # 根據感官輸入模擬心情轉折與真人對話
        if "敵人" in sensory_input or "危險" in sensory_input:
            self.current_mood = "alert / 警戒緊張"
            speech = "警告！偵測到潛在威脅，身體準備進入防禦與移動狀態！"
            action = "EVADE_AND_PREPARE"
            speed = 150
        elif "探索" in sensory_input:
            self.current_mood = "excited / 興奮探索"
            speech = "太棒了！前方有新的區域可以探索，我們出發吧！"
            action = "MOVE_FORWARD"
            speed = 100
        else:
            self.current_mood = "calm / 平靜思索"
            speech = "環境一切正常，我在這裡思考下一步的計畫。"
            action = "PATROL"
            speed = 50

        print(f"-> 🎭 [大腦心情]: {self.current_mood}")
        print(f"-> 🗣️ [真人語音/說話]: 『{speech}』")

        payload = {
            "mood": self.current_mood,
            "speech": speech,
            "action": action,
            "speed": speed
        }

        self.transmit_to_body(payload)

    def transmit_to_body(self, payload):
        """將大腦的意志與指令透過網路傳送給機器人身體"""
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.body_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            print(f"-> 🚀 [意志傳輸] 正在將大腦指令同步給機器人身體...")
            with urllib.request.urlopen(req, timeout=3) as res:
                result = json.loads(res.read().decode('utf-8'))
                print(f"-> [✔] 身體執行回報: {result}")
        except Exception as e:
            print(f"-> [❌] 無法連線至機器人身體: {e}")

if __name__ == "__main__":
    brain = AIMasterBrain()
    # 模擬 AI 大腦接收到環境感官刺激後做出反應
    brain.perceive_and_decide("前方發現未知區域需要進行探索")

