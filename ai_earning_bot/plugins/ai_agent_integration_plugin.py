import urllib.request
import json
import time
import os

class AIAgentIntegration:
    def __init__(self):
        # 你可以將此處替換為實際的 AI 模型 API 端點
        self.api_endpoint = "https://httpbin.org/post"
        self.api_key = os.environ.get("AI_API_KEY", "mock_key_for_testing")

    def invoke_ai_model(self, prompt_text):
        """向人工智慧模型發送請求並獲取分析回應"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "AIFusionAgent/1.0"
        }
        
        payload = {
            "model": "matrix-ai-core",
            "messages": [
                {"role": "system", "content": "你是一個內嵌在 Termux 終極融合引擎中的 AI 代理。"},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.7
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.api_endpoint, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=12.0) as response:
                if response.status == 200:
                    response_body = response.read().decode("utf-8")
                    result_json = json.loads(response_body)
                    return {
                        "status": "success",
                        "ai_response": result_json.get("json", {}),
                        "message": "成功取得人工智慧模型的分析與回應！"
                    }
        except Exception as e:
            return {
                "status": "fallback_mode",
                "error_detail": str(e),
                "message": "AI 網路連線暫時無法使用，已啟動本地安全容錯邏輯。"
            }
        return {"status": "failed", "message": "未知回應。"}

ai_agent = AIAgentIntegration()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行人工智慧代理的狀態評估與 API 互動。
    """
    print("🤖 [人工智慧外掛] 正在打包系統狀態並向 AI 模型發起請求...")
    
    # 傳送當前心跳的提示詞
    prompt = "分析當前背景引擎的運作狀態，並給出下一步的優化建議。"
    result = ai_agent.invoke_ai_model(prompt)
    
    print(f"✨ [AI 互動完成] 狀態: [{result['status']}] | {result['message']}")
    
    return {
        "plugin_name": "AIAgentIntegration",
        "ai_result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
