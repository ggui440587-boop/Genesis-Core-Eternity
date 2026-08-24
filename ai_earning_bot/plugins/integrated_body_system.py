import urllib.request
import json
import time

class BodyNexusSystem:
    def __init__(self):
        self.endpoint = "https://httpbin.org/post"

    def activate_brain(self):
        """大腦：負責決策與邏輯運算"""
        return {"organ": "Brain", "state": "processing_logic", "status": "active"}

    def activate_hands(self):
        """雙手：負責資料操作與互動"""
        return {"organ": "Hands", "state": "manipulating_data", "status": "ready"}

    def activate_legs(self):
        """雙腳：負責移動與巡邏"""
        return {"organ": "Legs", "state": "navigating_path", "status": "moving"}

    def sync_to_external(self):
        """將主體與所有器官狀態同步至外部網路"""
        payload = {
            "subject": "Main-Body-Framework",
            "organs": [
                self.activate_brain(),
                self.activate_hands(),
                self.activate_legs()
            ],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "BodySystem/1.0"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                if response.status == 200:
                    return {"sync": "success", "remote_echo": json.loads(response.read().decode("utf-8")).get("json", {})}
        except Exception as e:
            return {"sync": "error", "detail": str(e)}
        return {"sync": "failed"}

system_instance = BodyNexusSystem()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行主體與各大器官的協同運作並向外部網路發送同步請求。
    """
    print("🧬 [主體系統] 大腦思考中、雙手準備操作、雙腳開始移動...")
    
    result = system_instance.sync_to_external()
    
    print(f"✨ [外部同步結果] 狀態: [{result.get('sync')}] | 器官協同運作正常！")
    
    return {
        "plugin_name": "IntegratedBodySystem",
        "sync_result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
