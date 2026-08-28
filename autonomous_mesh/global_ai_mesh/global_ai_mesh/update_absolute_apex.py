with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 升級伺服器，加入邊緣叢集、硬體感測迴圈與強化學習獎勵引擎
apex_injection = """
# === 邊緣叢集調度、環境感測與強化學習獎勵模組 ===
import random

class EdgeClusterOrchestrator:
    def __init__(self):
        self.cluster_nodes = ["TERMUX_MASTER", "EDGE_NODE_SECONDARY"]

    def balance_load(self, task_name):
        target_node = random.choice(self.cluster_nodes)
        return f"Offloaded task {task_name} to {target_node}"

class PhysicalDigitalLoop:
    def __init__(self):
        self.sensors_active = True

    def poll_environment(self):
        # 模擬讀取硬體狀態與環境感測
        return {"network": "Stable", "battery_optimized": True}

class ReinforcementLearningEngine:
    def __init__(self):
        self.reward_score = 100.0

    def evaluate_and_adapt(self, success: bool):
        if success:
            self.reward_score += 1.5
        else:
            self.reward_score -= 2.0
        return self.reward_score
"""

if "EdgeClusterOrchestrator" not in code:
    code = apex_injection + "\n" + code
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully injected Edge Cluster, Sensor Loop & RL Engine!")
else:
    print("Apex ecosystem modules already exist.")
