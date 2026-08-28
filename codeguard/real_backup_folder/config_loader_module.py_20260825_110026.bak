import json
import os

class ConfigLoaderModule:
    def __init__(self, config_path="genesis_config.json"):
        self.config_path = config_path

    def load_config(self):
        print("-> ⚙️ [ConfigLoader] 正在載入系統設定檔...")
        if not os.path.exists(self.config_path):
            print("   [!] 找不到設定檔，將使用預設參數。")
            return {"interval": 3600, "mode": "production"}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                print("   [✓] 系統設定檔載入成功。")
                return config_data
        except Exception as e:
            print(f"   [✕] 解析設定檔發生異常: {e}")
            return {}

if __name__ == "__main__":
    loader = ConfigLoaderModule()
    loader.load_config()

