import pathlib
import time
import json

class CodeMetricsAnalyzer:
    def __init__(self):
        self.target_dir = pathlib.Path.cwd()

    def analyze_codebase(self):
        """掃描當前目錄下的所有 .py 檔案並計算程式碼度量指標"""
        py_files = list(self.target_dir.glob("*.py"))
        total_files = len(py_files)
        total_lines = 0
        file_stats = []

        for py_file in py_files:
            if py_file.name == "matrix_ultimate_fusion_engine.py":
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                lines = len(content.splitlines())
                total_lines += lines
                file_stats.append({
                    "filename": py_file.name,
                    "lines": lines
                })
            except Exception as e:
                print(f"⚠️ [分析例外] 無法讀取檔案 {py_file.name}: {e}")

        return {
            "total_python_files": total_files,
            "total_code_lines": total_lines,
            "details": file_stats
        }

analyzer = CodeMetricsAnalyzer()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行程式碼度量分析並輸出結果。
    """
    print("📊 [程式碼分析外掛] 正在掃描並計算專案中的程式碼結構與行數...")
    
    metrics = analyzer.analyze_codebase()
    
    print(f"✨ [分析完成] 已掃描 {metrics['total_python_files']} 個檔案，總程式碼行數: {metrics['total_code_lines']} 行")
    
    return {
        "plugin_name": "CodeMetricsAnalyzer",
        "metrics_result": metrics,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
