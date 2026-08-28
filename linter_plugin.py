import py_compile
import os

class LinterPlugin:
    def __init__(self):
        print("-> 🔍 [品質外掛] 初始化程式碼結構與語法檢查器...")

    def check_syntax(self):
        """檢查專案中所有 Python 檔案的語法是否正確無誤"""
        py_files = [f for f in os.listdir(".") if f.endswith(".py")]
        errors = 0
        
        for file in py_files:
            try:
                py_compile.compile(file, doraise=True)
            except Exception as e:
                print(f"-> ❌ [品質外掛] 檔案語法錯誤: {file} -> {e}")
                errors += 1
                
        if errors == 0:
            print(f"-> ✅ [品質外掛] 驗證完畢！全部 {len(py_files)} 個 Python 模組語法完全正確，結構完美。")
        return errors == 0

if __name__ == "__main__":
    linter = LinterPlugin()
    linter.check_syntax()
