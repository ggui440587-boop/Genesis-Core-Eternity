import os

class LogAnalyzerModule:
    def __init__(self, log_path="genesis_system.log"):
        self.log_path = log_path

    def analyze_logs(self):
        print("-> 🔍 [LogAnalyzer] 開始掃描與分析系統日誌...")
        if not os.path.exists(self.log_path):
            print("   [!] 找不到系統日誌檔案。")
            return

        error_count = 0
        warning_count = 0

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if "ERROR" in line or "異常" in line:
                    error_count += 1
                elif "WARNING" in line:
                    warning_count += 1

        print(f"   [✓] 分析完成：發現 {error_count} 個錯誤訊息，{warning_count} 個警告訊息。")
        return error_count

if __name__ == "__main__":
    analyzer = LogAnalyzerModule()
    analyzer.analyze_logs()

