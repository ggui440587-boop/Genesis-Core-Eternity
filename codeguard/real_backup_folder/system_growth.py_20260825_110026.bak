import json
import os

# ==============================================================
# System Growth & Evolution Module - 系統生長與自動升級模組
# ==============================================================

CONFIG_FILE = "genesis_config.json"

class SystemGrowth:
    @staticmethod
    def evolve_system(new_capability_name):
        """模擬系統生長：動態解鎖新能力並升級版本紀錄"""
        print("=" * 60)
        print(f" 🌱 [系統生長] 生態系正在經歷演化，準備融合新能力: [{new_capability_name}]")
        print("=" * 60)

        # 讀取現有基因設定
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)

        # 進行版本升級與能力擴充
        current_version = config.get("version", "1.0.0")
        parts = current_version.split(".")
        # 將版號的小版本號 + 1 (模擬生長演進)
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = ".".join(parts)

        config["version"] = new_version

        # 將新能力加入設定中
        if "capabilities" not in config:
            config["capabilities"] = []
        if new_capability_name not in config["capabilities"]:
            config["capabilities"].append(new_capability_name)

        # 寫回基因設定檔
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        print(f"[生長成功] 系統已成功進化至版本: {new_version}")
        print(f"-> 當前解鎖的所有能力清單: {config['capabilities']}")

if __name__ == "__main__":
    SystemGrowth.evolve_system("Autonomous-Self-Replication-Engine")

