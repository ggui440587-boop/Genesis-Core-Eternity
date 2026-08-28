import os
import importlib
import time
import sys

class HotReloadFactory:
    def __init__(self, plugin_name="plugin_module"):
        self.plugin_name = plugin_name
        self._create_dummy_plugin_if_not_exists()

    def _create_dummy_plugin_if_not_exists(self):
        plugin_file = f"{self.plugin_name}.py"
        if not os.path.exists(plugin_file):
            with open(plugin_file, "w", encoding="utf-8") as f:
                f.write("def run_logic():\n    print('-> 🧬 [外掛模組] 執行初始版本邏輯 v1')\n")

    def run_dynamic_loop(self):
        print("【動態熱載入外掛工廠啟動】")
        print("-> 💡 提示：你可以隨時修改 plugin_module.py 的內容，工廠會自動在運行中載入最新程式碼！\n")
        
        try:
            while True:
                # 動態導入或重新載入模組
                if self.plugin_name in sys.modules:
                    module = importlib.reload(sys.modules[self.plugin_name])
                else:
                    module = importlib.import_module(self.plugin_name)
                
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] -> 🔄 正在執行熱載入模組...")
                module.run_logic()
                
                print("-> 💤 暫停 5 秒，嘗試修改 plugin_module.py 看看...\n")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n-> 🛑 程式已安全終止。")

if __name__ == "__main__":
    factory = HotReloadFactory()
    factory.run_dynamic_loop()
