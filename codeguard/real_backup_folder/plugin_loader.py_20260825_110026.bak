import os
import importlib.util

# ==============================================================
# Plugin Loader Module - 動態外掛載入器模組
# ==============================================================

class PluginLoader:
    PLUGIN_DIR = "plugins"

    @classmethod
    def load_all_plugins(cls):
        """自動掃描並載入 plugins 資料夾底下的所有外掛模組"""
        print("=" * 60)
        print(" 🧩 [外掛載入] 正在掃描 Genesis-Core-Eternity 外掛目錄...")
        print("=" * 60)

        if not os.path.exists(cls.PLUGIN_DIR):
            os.makedirs(cls.PLUGIN_DIR)
            print(f"-> 📁 已自動建立外掛目錄: {cls.PLUGIN_DIR}/")

        plugin_files = [f for f in os.listdir(cls.PLUGIN_DIR) if f.endswith(".py")]

        if not plugin_files:
            print("-> ⚠️ 目前沒有發現任何外掛檔案。")
            return

        for filename in plugin_files:
            plugin_name = filename[:-3]
            file_path = os.path.join(cls.PLUGIN_DIR, filename)

            try:
                spec = importlib.util.spec_from_file_location(plugin_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"-> 🟢 [載入成功] 外掛 [{plugin_name}] 已成功掛載！")

                # 若外掛含有 run 函數則自動執行
                if hasattr(module, "run"):
                    module.run()
            except Exception as e:
                print(f"-> 🔴 [載入失敗] 外掛 [{plugin_name}] 發生錯誤: {e}")

        print("=" * 60)

if __name__ == "__main__":
    PluginLoader.load_all_plugins()

