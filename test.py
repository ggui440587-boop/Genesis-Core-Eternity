import requests

GROQ_API_KEY = "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"

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-70b-8192",
    "messages": [
        {"role": "user", "content": "測試連線，請回覆『連線成功』"}
    ]
}

response = requests.post(url, headers=headers, json=payload)
print("狀態碼:", response.status_code)
print("回應內容:", response.text)

