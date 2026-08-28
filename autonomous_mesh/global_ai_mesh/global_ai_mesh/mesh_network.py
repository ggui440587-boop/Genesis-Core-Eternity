import asyncio
import json


class P2PMeshNode:

  def __init__(self, host: str, port: int):
    self.host = host
    self.port = port
    self.peers = set()
    self.state = {"entropy": 0.5, "active_tasks": 0, "code_genes": []}

  async def handle_peer(self, reader, writer):
    data = await reader.read(1024)
    if not data:
      return
    try:
      message = json.loads(data.decode("utf-8"))
      if message.get("type") == "SYNC_STATE":
        peer_state = message.get("state", {})
        self.state["entropy"] = (
            self.state["entropy"] + peer_state.get("entropy", 0.5)
        ) / 2
    except Exception:
      pass
    writer.close()
    await writer.wait_closed()

  async def start_server(self):
    server = await asyncio.start_server(
        self.handle_peer, self.host, self.port
    )
    print(f"🌐 [P2P 網路] 節點已上線，監聽於 {self.host}:{self.port}")
    async with server:
      await server.serve_forever()

  async def broadcast_to_peers(self, message: dict):
    for peer_host, peer_port in self.peers:
      try:
        reader, writer = await asyncio.open_connection(peer_host, peer_port)
        writer.write(json.dumps(message).encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()
      except Exception:
        pass

