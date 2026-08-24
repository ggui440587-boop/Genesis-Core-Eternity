import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 替換為真實的 Groq API 呼叫邏輯
old_func = """def analyze_with_retry(title, retries=3, delay=2):
    \"\"\"具備自動重試機制的本地/AI 分析模組\"\"\"
    for attempt in range(retries):
        try:
            # 如果沒有設定真實金鑰，使用高質感本地智慧模擬
            if not GROQ_API_KEY or GROQ_API_KEY.startswith("你的"):
                return f"[本地穩健分析] 標題：{title}。具備高價值技術參考，系統自動評估通過。\"\"
            
            # 若有金鑰，此處可擴充真實 API 呼叫，目前以穩健防禦為主
            return f"[雲端智慧分析] 標題：{title}。核心亮點：高自主性架構與行動端運算價值。"
        except Exception as e:
            log_message("WARNING", "分析嘗試失敗 (第 %d 次): %s" % (attempt + 1, e))
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return f"[解析降級] 達到最大重試次數，標題：{title}\""""

new_func = """def analyze_with_retry(title, retries=3, delay=2):
    \"\"\"真實呼叫 Groq API 的雲端大腦模組\"\"\"
    import urllib.request
    import json
    for attempt in range(retries):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": f"請用精鍊的繁體中文，針對以下技術標題撰寫一段 50 字以內的專業技術摘要：{title}"}],
                "temperature": 0.5
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_data = json.loads(resp.read().decode())
                summary = res_data['choices'][0]['message']['content'].strip()
                return summary
        except Exception as e:
            log_message("WARNING", f"Groq API 呼叫失敗 (第 {attempt + 1} 次): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return f"[真實解析失敗] 標題：{title} (錯誤: {e})" """

if old_func in content:
    content = content.replace(old_func, new_func)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] 成功將主程式升級為 100% 真實 Groq API 雲端運算！")
else:
    print("[INFO] 結構已更新或需手動對齊。")
