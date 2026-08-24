import json
import os

# ==============================================================
# Config Manager Module - 參數自訂與動態修改管理模組
# ==============================================================

class ConfigManager:
    CONFIG_FILE = "ecosystem_config.json"

    @classmethod
    def get_config(cls):
        """讀取現有的設定檔，若不存在則建立預設值"""
        if not os.path.exists(cls.CONFIG_FILE):
            default_data = {
                "app_name": "Genesis-Core-Eternity",
                "max_retries": 3,
                "environment": "Termux-Mobile",
                "debug_mode": True
            }
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)

        with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def update_parameter(cls, key, value):
        """讓你可以動態自訂並修改指定的參數"""
        config = cls.get_config()
        if key in config:
            old_value = config[key]
            config[key] = value
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print(f"🔧 [參數自訂成功] 屬性 [{key}] 已從 {old_value} 修改為：{value}")
        else:
            print(f"⚠️ [參數錯誤] 找不到指定的參數鍵值: [{key}]")

if __name__ == "__main__":
    # 測試自訂修改參數：將 max_retries（最大重試次數）改為 5
    print("--- 修改前的設定 ---")
    print(ConfigManager.get_config())

    print("\n--- 正在執行自訂修改 ---")
    ConfigManager.update_parameter("max_retries", 5)

    print("\n--- 修改後的最新設定 ---")
    print(ConfigManager.get_config())

