import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ZeroRiskFusionBrain:
    def __init__(self):
        print("🔒 [0風險安全融合大腦] 系統啟動中...")
        self.providers = {
            "groq": {
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "key": os.getenv("GROQ_API_KEY"),
                "model": "openai/gpt-oss-120b"
            },
            "deepseek": {
                "url": "https://api.deepseek.com/v1/chat/completions",
                "key": os.getenv("DEEPSEEK_API_KEY"),
                "model": "deepseek-chat"
            },
            "qwen": {
                "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                "key": os.getenv("QWEN_API_KEY"),
                "model": "qwen-max"
            },
            "xai": {
                "url": "https://api.x.ai/v1/chat/completions",
                "key": os.getenv("XAI_API_KEY"),
                "model": "grok-beta"
            },
            "nvidia": {
                "url": "https://integrate.api.nvidia.com/v1/chat/completions",
                "key": os.getenv("NVIDIA_API_KEY"),
                "model": "meta/llama-3.1-70b-instruct"
            },
            "openai": {
                "url": "https://api.openai.com/v1/chat/completions",
                "key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4o"
            }
        }

    def ask_all(self, prompt: str):
        active_count = 0
        for name, info in self.providers.items():
            if not info["key"] or "請填入" in info["key"] or "你的" in info["key"]:
                continue
                
            active_count += 1
            print(f"\n" + "-"*50)
            print(f"🛡️ 正在呼叫大腦: [{name.upper()}] (模型: {info['model']})...")
            print("-"*50)
            
            headers = {
                "Authorization": f"Bearer {info['key']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": info["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            try:
                response = requests.post(info["url"], headers=headers, json=payload, timeout=20)
                if response.status_code == 200:
                    ans = response.json()["choices"][0]["message"]["content"]
                    print(f"💡 [{name.upper()}] 回答：\n{ans}\n")
                else:
                    print(f"⚠️ [{name.upper()}] 狀態異常 ({response.status_code})，已安全略過。\n")
            except requests.exceptions.Timeout:
                print(f"⚠️ [{name.upper()}] 連線逾時，已自動跳過。\n")
            except Exception as e:
                print(f"⚠️ [{name.upperM() if 'M' in name else name.upper()}] 發生預期外例外，安全攔截。\n")
                
        if active_count == 0:
            print("🔒 [安全提示] 目前沒有偵測到任何合法的有效金鑰。請確認您的 .env 檔案是否有確實填入。")

if __name__ == "__main__":
    brain = ZeroRiskFusionBrain()
    print("\n✅ 0風險安全融合大腦已就緒！")
    
    while True:
        try:
            user_input = input("\n🎯 總指揮請下達指令 (輸入 q 離開): ").strip()
            if user_input.lower() == 'q':
                print("👋 正在安全關閉大腦系統，再見！")
                break
            if not user_input:
                continue
                
            brain.ask_all(user_input)
        except KeyboardInterrupt:
            print("\n👋 系統已安全中斷。")
            break
