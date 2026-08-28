import glob
import os

class ComplexityCheckerPlugin:
    def __init__(self, target_extension="_plugin.py"):
        self.target_extension = target_extension
        print("-> 📊 [複雜度分析外掛] 系統架構評估器初始化成功！")

    def audit_project(self):
        """掃描當前目錄下的外掛數量與程式碼行數，評估是否過度設計"""
        pattern = f"*{self.target_extension}"
        plugin_files = glob.glob(pattern)
        total_plugins = len(plugin_files)
        
        total_lines = 0
        for filepath in plugin_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                total_lines += sum(1 for _ in f)

        print(f"\n--- 📈 專案程式碼健檢報告 ---")
        print(f"-> 📦 總外掛模組數量: {total_plugins}")
        print(f"-> 📝 總程式碼行數 (LOC): {total_lines}")
        
        if total_plugins > 10:
            print("-> ⚠️ [工程警示] 外掛數量已超過 10 個！系統可能出現『過度設計 (Over-engineering)』，建議進行模組合併或重構。")
        else:
            print("-> ✅ [工程狀態] 模組數量適中，架構保持在健康範圍。")
        print("----------------------------\n")

if __name__ == "__main__":
    checker = ComplexityCheckerPlugin()
    checker.audit_project()
