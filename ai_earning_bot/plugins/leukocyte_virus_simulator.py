import urllib.request
import json
import time
import random

class Virus:
    def __init__(self):
        self.strain = random.choice(["Alpha-Payload", "Beta-Infiltrator", "Null-Anomaly"])
        self.threat_level = round(random.uniform(0.3, 0.9), 2)

    def mutate(self):
        """模擬病毒的變異與動態入侵行為"""
        return {
            "entity": "Virus",
            "strain": self.strain,
            "threat_level": self.threat_level,
            "status": "active_infiltration"
        }

class Leukocyte:
    def __init__(self):
        self.cell_id = "Leukocyte-Core-01"

    def scan_and_neutralize(self, virus_data):
        """模擬白血球偵測病毒並進行防禦清理的邏輯"""
        is_neutralized = virus_data["threat_level"] < 0.7
        return {
            "entity": "Leukocyte",
            "defender_id": self.cell_id,
            "action": "neutralized" if is_neutralized else "contained_resistance",
            "success": is_neutralized
        }

class ImmuneSystemSimulation:
    def __init__(self):
        self.virus = Virus()
        self.leukocyte = Leukocyte()
        self.endpoint = "https://httpbin.org/post"

    def execute_simulation(self):
        """執行白血球與病毒的對抗循環，並向外部網路同步狀態"""
        virus_status = self.virus.mutate()
        defense_result = self.leukocyte.scan_and_neutralize(virus_status)
        
        payload = {
            "system_architecture": "Leukocyte-Virus-Defense-Simulator",
            "virus_layer": virus_status,
            "defense_layer": defense_result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "ImmuneSimulator/1.0"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                if response.status == 200:
                    return {"status": "success", "remote_echo": json.loads(response.read().decode("utf-8")).get("json", {})}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
        return {"status": "failed"}

# 實例化免疫模擬系統
immune_sim = ImmuneSystemSimulation()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行白血球與病毒的程式化對抗模擬。
    """
    print("🛡️ [免疫系統] 白血球正在掃描系統，偵測潛在的病毒入侵因子...")
    
    result = immune_sim.execute_simulation()
    
    print(f"✨ [防禦同步完成] 狀態: [{result.get('status')}] | 免疫對抗循環運作正常！")
    
    return {
        "plugin_name": "LeukocyteVirusSimulator",
        "simulation_result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
