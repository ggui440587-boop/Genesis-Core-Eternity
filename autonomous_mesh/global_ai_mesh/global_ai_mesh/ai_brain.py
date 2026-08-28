import aiohttp
import json


class AIBrain:

  def __init__(self, ollama_url="http://localhost:11434/api/generate"):
    self.ollama_url = ollama_url
    self.model_name = "llama3"

  async def think_proactively(self, system_state: dict) -> dict:
    prompt = f"""
        你是一個全球分散式 AI 網體的自主節點。
        目前系統狀態：{json.dumps(system_state)}
        請根據目前狀態，自主決定下一步要執行的動作。
        必須以純 JSON 格式回應，包含兩個欄位："action" (選擇 analyze_logs, scan_network, 或 optimize_memory) 與 "payload" (執行細節)。
        """
    payload = {
        "model": self.model_name,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    try:
      async with aiohttp.ClientSession() as session:
        async with session.post(
            self.ollama_url, json=payload, timeout=10
        ) as resp:
          result = await resp.json()
          return json.loads(result.get("response", "{}"))
    except Exception:
      return {"action": "analyze_logs", "payload": "fallback_routine"}

