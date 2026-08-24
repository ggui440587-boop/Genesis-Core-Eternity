import json
import os

# ==============================================================
# Config Loader Module - 全域應用設定與參數管理模組
# ==============================================================

class ConfigLoader:
    CONFIG_FILE = "ecosystem_config.json"

    @classmethod
    def init_default_config(cls):
        """若設定檔不存在，自動建立預設的應用參數"""
        if not os.path.exists(cls.CONFIG_FILE):
            default_data = {
                "app_name": "Genesis-Core-Eternity",
                "version": "1.0.0",
                "max_retries": 3,
                "environment": "Termux-Mobile",
                "debug_mode": True
            }
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
            print(f"⚙️ [設定檔初始化] 已成功建立預設參數檔: [{cls.CONFIG_FILE}]")

    @classmethod
    def load_config(cls):
        """讀取應用參數"""
        cls.init_default_config()
        with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"🔧 [設定載入] 成功載入應用程式: {config['app_name']} (版本: {config['version']})")
        return config

if __name__ == "__main__":
    ConfigLoader.load_config()

