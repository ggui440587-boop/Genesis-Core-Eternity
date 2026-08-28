import os
import importlib.util

class PluginLoaderModule:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir

    def load_plugins(self):
        print("-> 🔌 [PluginLoader] 開始掃描與載入動態外掛...")
        if not os.path.exists(self.plugin_dir):
            print("   [!] 找不到外掛資料夾。")
            return

        loaded_count = 0
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]
                plugin_path = os.path.join(self.plugin_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "run_plugin"):
                        module.run_plugin()
                        print(f"   [✓] 成功載入並執行外掛: {plugin_name}")
                        loaded_count += 1
                except Exception as e:
                    print(f"   [✕] 載入外掛 {plugin_name} 失敗: {e}")

        print(f"   [✓] 外掛載入完畢，共成功執行 {loaded_count} 個外掛。")

if __name__ == "__main__":
    loader = PluginLoaderModule()
    loader.load_plugins()

