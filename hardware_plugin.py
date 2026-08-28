import subprocess
import shutil
import json

class HardwarePlugin:
    def __init__(self):
        self.has_api = shutil.which("termux-battery-status") is not None

    def get_battery_status(self):
        """透過 Termux API 取得手機電池與充電狀態"""
        if not self.has_api:
            return {"percentage": 100, "status": "UNKNOWN (No API)"}

        try:
            result = subprocess.run(
                ["termux-battery-status"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return {
                "percentage": data.get("percentage", 0),
                "status": data.get("status", "UNKNOWN"),
                "temperature": data.get("temperature", 0)
            }
        except Exception as e:
            print(f"-> ⚠️ [硬體外掛] 讀取電池失敗: {e}")
            return {"percentage": 0, "status": "ERROR"}

if __name__ == "__main__":
    hw = HardwarePlugin()
    print("Battery Info:", hw.get_battery_status())
