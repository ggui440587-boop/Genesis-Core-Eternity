import json
import urllib.request
import datetime

class AIAssistant:
    def __init__(self):
        print("-> 🤖 [AI 助理] 初始化完成！準備建立對話通道。")
        self.conversation_history = []

    def chat_loop(self):
        """啟動互動式對話迴圈"""
        print("-> 💡 [提示] 輸入你的問題後按下 Enter (輸入 'exit' 即可離開程式)\n")

        while True:
            try:
                user_input = input("你: ")
                if user_input.lower() == 'exit':
                    print("-> 🤖 [AI 助理] 期待下次再見！")
                    break

                if not user_input.strip():
                    continue

                # 紀錄對話歷史
                self.conversation_history.append({"role": "user", "content": user_input})

                # 模擬 AI 思考與回應（實際開發時可在此處替換為真實的 API 請求）
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                ai_reply = f"這是模擬市面 AI 的回應 [{timestamp}]：我已收到你的訊息『{user_input}』，並正在為你處理！"

                print(f"AI: {ai_reply}\n")
                self.conversation_history.append({"role": "assistant", "content": ai_reply})

            except KeyboardInterrupt:
                print("\n-> 🤖 [AI 助理] 程式已安全中斷。")
                break

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.chat_loop()

