import urllib.request
import json
import time

class ExternalNetworkBridge:
    def __init__(self):
        self.endpoint = "https://httpbin.org/post"

    def send_external_sync(self):
        """將狀態透過外部網路進行同步"""
        payload = {
            "plugin": "ExternalNetworkBridge",
            "status": "syntax_fixed_and_active",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ExternalBridge/1.0"
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                if response.status == 200:
                    response_body = response.read().decode("utf-8")
                    return {
                        "status": "success",
                        "echo": json.loads(response_body).get("json", {})
                    }
        except Exception as e:
            return {
                "status": "error",
                "detail": str(e)
            }
        return {"status": "failed"}

bridge_instance = ExternalNetworkBridge()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行修正後的外部網路同步任務。
    """
    print("🌐 [外部網路外掛] 正在執行網路同步...")
    
    result = bridge_instance.send_external_sync()
    
    print(f"✨ [外部同步結果] 狀態: [{result.get('status')}] | 括號與語法已完全修正！")
    
    return {
        "plugin_name": "ExternalNetworkBridge",
        "result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
