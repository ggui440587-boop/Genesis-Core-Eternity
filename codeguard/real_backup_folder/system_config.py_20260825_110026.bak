import json
import os

# ==============================================================
# System Config & Skin Module - 系統基因設定與對外邊界防護 (象徵皮膚與DNA)
# ==============================================================

CONFIG_FILE = "genesis_config.json"

def init_system_config():
    """初始化系統的基因設定檔（如版本、心跳速率、連線埠等）"""
    default_config = {
        "system_name": "Genesis-Core-Eternity",
        "version": "1.0.0",
        "heart_rate_seconds": 5,
        "environment": "Termux-Android",
        "security_mode": "ACTIVE"
    }

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print(f"[基因設定] 已成功建立預設系統設定檔: {CONFIG_FILE}")
    else:
        print(f"[基因設定] 讀取現有系統設定檔: {CONFIG_FILE}")

def load_config():
    """讀取系統設定"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

if __name__ == "__main__":
    print("=" * 60)
    print(" 🧬 系統基因與外在設定模組啟動")
    print("=" * 60)
    init_system_config()
    config = load_config()
    print(f"-> 當前系統名稱: {config['system_name']} (版本: {config['version']})")
    print(f"-> 防護邊界狀態: {config['security_mode']}")

