with open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

# 升級 AIBrain，加入智慧重試與降級容錯
old_ai_class = """class AIBrain:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/generate"

    async def think_proactively(self, state):
        prompt = f"You are an absolute ultimate secure & real-pipeline AI agent in Termux. Current state: {json.dumps(state)}.\\nReturn ONLY a valid JSON object with keys: \\"speech\\" (short lively Traditional Chinese sentence), \\"action\\" (string), \\"goal\\" (current objective), \\"security_status\\" (string like 'ENV-SECURE-LOCKED'), \\"filename\\" (optional script name), \\"evolution_code\\" (optional python code restricted to sandbox)."
        req_data = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        req = urllib.request.Request(self.url, data=req_data, headers={"Content-Type": "application/json"})
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=4))
            res_body = json.loads(response.read().decode("utf-8"))
            raw_text = res_body.get("response", "{}").strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            return json.loads(raw_text)
        except Exception:
            return {
                "speech": "資安防護隔離正常，真實情報與雲端管線全速運作中！",
                "action": "資安稽核與真實情報抓取",
                "goal": "實現 100% 安全且真實的無人自動化營運",
                "security_status": "ENV-SECURE-ACTIVE",
                "filename": "security_check.py",
                "evolution_code": "import os; print('Environment Security Check Passed, Secrets Isolated:', 'TELEGRAM_BOT_TOKEN' in os.environ or True)"
            }"""

new_ai_class = """class AIBrain:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/generate"

    async def think_proactively(self, state):
        prompt = f"You are an absolute ultimate secure & real-pipeline AI agent in Termux. Current state: {json.dumps(state)}.\\nReturn ONLY a valid JSON object with keys: \\"speech\\" (short lively Traditional Chinese sentence), \\"action\\" (string), \\"goal\\" (current objective), \\"security_status\\" (string like 'ENV-SECURE-LOCKED'), \\"filename\\" (optional script name), \\"evolution_code\\" (optional python code restricted to sandbox)."
        req_data = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        req = urllib.request.Request(self.url, data=req_data, headers={"Content-Type": "application/json"})
        
        # 智慧重試機制 (Retries with Fallback)
        for attempt in range(2):
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=3))
                res_body = json.loads(response.read().decode("utf-8"))
                raw_text = res_body.get("response", "{}").strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                return json.loads(raw_text)
            except Exception:
                if attempt == 0:
                    await asyncio.sleep(1) # 短暫退避後重試
                    continue
        
        # 離線安全降級預設策略 (LLM Fallback Mode)
        return {
            "speech": "本地大模型暫時休眠，已自動啟動資安與情報自癒降級模式！",
            "action": "安全沙盒自癒與真實情報維持",
            "goal": "在離線與高防護狀態下維持 100% 穩定營運",
            "security_status": "ENV-SECURE-FALLBACK-ACTIVE",
            "filename": "resilience_check.py",
            "evolution_code": "import time, os; print('Resilience Fallback Check Executed at:', time.time())"
        }"""

if old_ai_class in content:
    content = content.replace(old_ai_class, new_ai_class)
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully upgraded server.py with LLM Smart Fallback!")
else:
    print("AI class pattern already updated or customized.")
