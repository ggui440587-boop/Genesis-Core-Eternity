import asyncio
import threading
from ai_brain import AIBrain
from mesh_network import P2PMeshNode
from secure_sandbox import SecureSandbox


class GlobalAutonomousAgent:

  def __init__(self, node_id: str, host: str, port: int):
    self.node_id = node_id
    self.mesh = P2PMeshNode(host, port)
    self.brain = AIBrain()
    self.sandbox = SecureSandbox()
    self.is_active = True

  async def evolutionary_mind_loop(self):
    print(f"[{self.node_id}] 🌟 全球自主演化引擎已全面啟動...")

    while self.is_active:
      current_state = {
          "node_id": self.node_id,
          "entropy": self.mesh.state["entropy"],
          "peers_count": len(self.mesh.peers),
      }

      intent = await self.brain.think_proactively(current_state)
      print(f"[{self.node_id}] 🧠 AI 自主意圖生成：{intent}")

      if "evolution_code" in intent:
        code_to_test = intent["evolution_code"]
        success, report = self.sandbox.run_in_isolated_process(code_to_test)
        if success:
          print(f"[{self.node_id}] 🧬 基因突變成功：{report}")
          await self.mesh.broadcast_to_peers({
              "type": "SYNC_GENE",
              "gene": code_to_test,
          })
        else:
          print(f"[{self.node_id}] 🛑 沙盒防護攔截：{report}")

      await self.mesh.broadcast_to_peers(
          {"type": "SYNC_STATE", "state": current_state}
      )
      await asyncio.sleep(10)


if __name__ == "__main__":
  agent = GlobalAutonomousAgent("TERMUX-GLOBAL-01", "127.0.0.1", 9000)

  threading.Thread(
      target=lambda: asyncio.run(agent.mesh.start_server()), daemon=True
  ).start()

  try:
    asyncio.run(agent.evolutionary_mind_loop())
  except KeyboardInterrupt:
    print("\n🔴 收到全域手動熔斷指令，系統安全關閉。")
    agent.is_active = False

