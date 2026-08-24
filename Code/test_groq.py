import requests
import json

api_key = "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"
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 使用目前支援的模型
payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": "請用繁體中文寫一句話：系統測試成功"}],
    "temperature": 0.7
}

print("正在重新發送請求至 Groq API...")
try:
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    print(f"HTTP 狀態碼: {response.status_code}")
    print(f"完整回應內容:\n{response.text}")
except Exception as e:
    print(f"發生例外錯誤: {e}")
