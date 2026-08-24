import urllib.request
import json
import time
import random

class CyborgSystem:
    def __init__(self):
        self.endpoint = "https://httpbin.org/post"

    def brain_think(self):
        """大腦：負責對外發起外部智慧決策與意識評估"""
        return {
            "organ": "Brain",
            "status": "active_external_cognition",
            "thought_process": "正在透過外部網路同步全域狀態與決策指令。"
        }

    def hands_manipulate(self):
        """雙手：負責外部資料的抓取與建構操作"""
        return {
            "organ": "Hands",
            "status": "ready_to_interact",
            "action_performed": "對外部端點進行資料抓取與封包建構。"
        }

    def legs_walk(self):
        """雙腳：負責在系統與網路路徑中進行巡邏與位移掃描"""
        return {
            "organ": "Legs",
            "status": "patrolling",
            "position": f"external_node_sector_{random.randint(1, 100)}"
        }

    def sync_with_external_world(self):
        """整合大腦與四肢，向外部網路發送完整狀態"""
        payload = {
            "system_structure": "Body + Brain + Hands + Legs",
            "brain": self.brain_think(),
            "hands": self.hands_manipulate(),
            "legs": self.legs_walk(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "CyborgNexus/1.0"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                if response.status == 200:
                    return {"sync_status": "success", "remote_echo": json.loads(response.read().decode("utf-8")).get("json", {})}
        except Exception as e:
            return {"sync_status": "offline", "error": str(e)}
        return {"sync_status": "failed"}

cyborg = CyborgSystem()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行主體外掛：大腦思考、雙手操作、雙腳巡邏，並全面向外部網路同步。
    """
    print("🤖 [生化機械體] 大腦啟動思考，雙手準備操作，雙腳開始巡邏...")
    
    result = cyborg.sync_with_external_world()
    
    print(f"✨ [四肢與大腦同步完成] 狀態: [{result['sync_status']}] | 結構運作正常！")
    
    return {
        "plugin_name": "CyborgLimbsAndBrain",
        "architecture": "Body + Brain + Hands + Legs (100% External)",
        "organs_status": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
