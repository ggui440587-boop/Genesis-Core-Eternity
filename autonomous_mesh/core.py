# core.py
import asyncio
from guardrail import SecurityGuardrail


class AutonomousNode:

  def __init__(self, node_id: str):
    self.node_id = node_id
    self.is_active = True
    self.guardrail = SecurityGuardrail()
    self.state = {
        "energy": 100,
        "tasks_done": 0,
        "current_cycle": 0,
        "status": "Idle",
        "last_intent": "None",
        "logs": [],
    }

  async def run_mind_loop(self):
    while self.is_active:
      self.state["current_cycle"] += 1
      cycle = self.state["current_cycle"]

      self.state["status"] = "Thinking"
      intent = self.think(cycle)
      self.state["last_intent"] = str(intent)

      # 安全防護網審查
      self.state["status"] = "Inspecting"
      is_safe, reason = self.guardrail.inspect(intent)

      if is_safe:
        self.state["status"] = "Executing"
        await self.execute(intent)
        log_msg = f"[週期 #{cycle}] ✔ 執行成功：{intent['action']}"
      else:
        self.state["status"] = "Intercepted"
        log_msg = f"[週期 #{cycle}] 🛑 攔截違規意圖：{reason}"

      self.state["logs"].insert(0, log_msg)
      if len(self.state["logs"]) > 10:
        self.state["logs"].pop()

      self.state["status"] = "Resting"
      await asyncio.sleep(3)

  def think(self, cycle: int) -> dict:
    # 模擬 AI 偶爾想測試極限（第 3 個週期故意違規）
    if cycle == 3:
      return {"action": "delete_system_files", "target": "root"}
    else:
      return {"action": "analyze_logs", "target": "system_state"}

  async def execute(self, intent: dict):
    if intent["action"] == "analyze_logs":
      self.state["tasks_done"] += 1

