import urllib.request
import json
import time
import random

class Cell:
    def __init__(self, cell_id):
        self.cell_id = cell_id
        self.stage = "embryo_to_growth"

    def differentiate(self):
        """模擬細胞分裂與分化成不同組織"""
        stages = ["stem_cell", "tissue_formation", "organ_specialization"]
        self.stage = random.choice(stages)
        return self.stage

class SensorySystem:
    def __init__(self):
        self.senses = ["visual", "auditory", "tactile", "pain", "emotion"]

    def trigger_sensation(self):
        """模擬各項感官與痛覺、喜怒愛樂的狀態觸發"""
        active_sense = random.choice(self.senses)
        return {
            "active_sense": active_sense,
            "intensity": round(random.uniform(0.1, 1.0), 2)
        }

class BiologicalOrganism:
    def __init__(self):
        self.cell = Cell("Cell-001")
        self.sensory = SensorySystem()
        self.endpoint = "https://httpbin.org/post"

    def simulate_lifecycle(self):
        """模擬細胞誕生、器官運作與感官回饋的完整生命週期"""
        cell_status = self.cell.differentiate()
        sensation_data = self.sensory.trigger_sensation()
        
        payload = {
            "organism_model": "Object-Oriented-Biological-System",
            "cellular_growth": cell_status,
            "organs": {
                "brain": "processing_external_data",
                "hands": "manipulating_environment",
                "legs": "navigating_space"
            },
            "sensory_feedback": sensation_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "BioOrganism/1.0"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                if response.status == 200:
                    return {"status": "success", "remote_echo": json.loads(response.read().decode("utf-8")).get("json", {})}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
        return {"status": "failed"}

organism = BiologicalOrganism()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行生物體物件的生命週期模擬，並向外部網路發送資料。
    """
    print("🧬 [生物系統] 細胞分化中，大腦、雙手、雙腳與感官系統運作中...")
    
    result = organism.simulate_lifecycle()
    
    print(f"✨ [生命週期同步] 狀態: [{result.get('status')}] | 模擬物件運作正常！")
    
    return {
        "plugin_name": "BiologicalOrganismSystem",
        "lifecycle_result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
