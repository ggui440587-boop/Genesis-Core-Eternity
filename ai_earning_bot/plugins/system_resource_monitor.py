import os
import time
import json

class SystemResourceMonitor:
    def __init__(self):
        self.plugin_name = "SystemResourceMonitor"

    def check_hardware_metrics(self):
        """以現實層面來說，獲取當前執行環境（Termux/Linux）的負載與記憶體狀態"""
        try:
            # 讀取 Linux 系統負載平均值
            load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
            
            metrics = {
                "system_load_1min": load_avg[0],
                "system_load_5min": load_avg[1],
                "environment": "Termux-Android-Daemon",
                "status": "healthy"
            }
            return metrics
        except Exception as e:
            return {
                "environment": "Termux-Android-Daemon",
                "status": "error",
                "detail": str(e)
            }

monitor_instance = SystemResourceMonitor()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行現實硬體資源的檢測與狀態回報。
    """
    print("📈 [資源監控外掛] 正在檢測現實系統硬體負載與運行狀態...")
    
    metrics = monitor_instance.check_hardware_metrics()
    
    print(f"✨ [監控完成] 系統負載 (1分鐘): [{metrics.get('system_load_1min', 'N/A')}] | 狀態: [{metrics.get('status')}]")
    
    return {
        "plugin_name": "SystemResourceMonitor",
        "resource_metrics": metrics,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
