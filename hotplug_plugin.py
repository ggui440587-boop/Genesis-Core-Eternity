import importlib
import sys

class HotPluggingPlugin:
    def __init__(self):
        print("-> 🔌 [熱插拔外掛] 動態模組載入器初始化成功！")

    def load_module(self, module_name):
        """動態載入指定的 Python 模組"""
        try:
            if module_name in sys.modules:
                # 若已載入則進行熱重載
                mod = importlib.reload(sys.modules[module_name])
                print(f"-> 🔄 [熱插拔] 模組 '{module_name}' 已成功重新載入 (Hot-Reloaded)。")
            else:
                # 首次動態載入
                mod = importlib.import_module(module_name)
                print(f"-> ✅ [熱插拔] 模組 '{module_name}' 已成功動態載入。")
            return mod
        except Exception as e:
            print(f"-> ❌ [熱插拔錯誤] 無法載入模組 '{module_name}': {e}")
            return None

if __name__ == "__main__":
    hp = HotPluggingPlugin()
    # 嘗試動態載入我們剛才建立的數學或系統模組作為測試
    hp.load_module("math")
