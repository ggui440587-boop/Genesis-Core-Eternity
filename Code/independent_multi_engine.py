import requests
import json

# 設定
api_key = "xai-M5BNgXq6wCOVpNeV9bXmNqmD6CuPA80P2I1SDZXQQwqdmMOk1YNSKJX8OfHLmpOUyvEbBEIOeIwqtF5w"
url = "https://api.x.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "grok-4.6",
    "messages": [
        {"role": "user", "content": "你好，請回傳一個 JSON 格式的科技影片標題，格式：{\"title\": \"測試\"}"}
    ]
}

print("🔄 正在發送請求至 xAI (使用 grok-4.6)...")
response = requests.post(url, headers=headers, json=data)

print(f"📡 狀態碼: {response.status_code}")
print(f"📄 回應內容: {response.text}")
