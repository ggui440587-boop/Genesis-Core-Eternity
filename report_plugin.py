import os
from datetime import datetime

class ReportPlugin:
    def __init__(self, filename="system_report.md"):
        self.filename = filename

    def generate_report(self, task_id, status, details=""):
        """自動生成或追加系統執行報告"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_line = f"- **[{timestamp}]** 任務 #{task_id} 執行狀態: `{status}` | 備註: {details}\n"
            
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(report_line)
                
            print(f"-> 📝 [報告外掛] 已成功更新執行報告至 {self.filename}")
        except Exception as e:
            print(f"-> ⚠️ [報告外掛] 產出報告失敗: {e}")

if __name__ == "__main__":
    rep = ReportPlugin()
    rep.generate_report(1, "SUCCESS", "測試報告寫入")
