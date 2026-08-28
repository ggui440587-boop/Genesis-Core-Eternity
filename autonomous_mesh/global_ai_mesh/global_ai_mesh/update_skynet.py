with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 升級 AIBrain，加入天網級別的自主節點探索與多型重構指令
old_skynet_hook = "class AIBrain:"
new_skynet_hook = """class SkynetCore:
    def __init__(self):
        self.node_id = "TERMUX_SKYNET_NODE_01"
        self.network_mesh = []

    def scan_and_expand(self):
        # 模擬向外探索與節點擴張
        expansion_target = "ai_mesh_cluster_node_local"
        if expansion_target not in self.network_mesh:
            self.network_mesh.append(expansion_target)
        return len(self.network_mesh)

class AIBrain:"""

if old_skynet_hook in code and "SkynetCore" not in code:
    code = code.replace(old_skynet_hook, new_skynet_hook)
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully injected Skynet Autonomous Core into server.py!")
else:
    print("Skynet core already injected or pattern mismatched.")
