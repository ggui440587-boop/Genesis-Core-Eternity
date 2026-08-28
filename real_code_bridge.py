import importlib.util
import os
import sys

class RealCodeBridge:
    def __init__(self, module_file_path):
        self.module_file_path = module_file_path

    def load_and_execute(self, function_name, *args, **kwargs):
        """動態載入現實世界中的外部 Python 程式碼檔案並執行指定函式"""
        if not os.path.exists(self.module_file_path):
            print(f"-> ⚠️ 找不到指定的程式碼檔案: {self.module_file_path}")
            return None

        module_name = os.path.splitext(os.path.basename(self.module_file_path))[0]
        
        try:
            # 動態載入外部真實 .py 檔案
            spec = importlib.util.spec_from_file_location(module_name, self.module_file_path)
            external_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = external_module
            spec.loader.exec_module(external_module)
            
            # 檢查並執行目標函式
            if hasattr(external_module, function_name):
                target_func = getattr(external_module, function_name)
                print(f"-> 🧬 [真實程式橋接] 成功載入並執行外部模組: {module_name}.{function_name}")
                return target_func(*args, **kwargs)
            else:
                print(f"-> ⚠️ 外部模組中找不到指定的函式: {function_name}")
                return None
        except Exception as e:
            print(f"-> ❌ 載入現實程式碼時發生錯誤: {e}")
            return None

if __name__ == "__main__":
    # 範例：假設我們把現實中的某個程式檔叫做 real_module.py
    sample_code = """
def real_world_task(name):
    return f"Hello, {name}! 這是一段從現實世界搬進來的真實程式碼執行結果。"
"""
    with open("real_module.py", "w", encoding="utf-8") as f:
        f.write(sample_code)

    # 透過橋接器載入並執行它
    bridge = RealCodeBridge("real_module.py")
    result = bridge.load_and_execute("real_world_task", "哲熙")
    print(result)
