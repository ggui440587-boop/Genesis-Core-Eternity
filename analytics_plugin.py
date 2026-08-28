import os

class AnalyticsPlugin:
    def __init__(self, log_file="system_actions.log"):
        self.log_file = log_file

    def analyze_stats(self):
        """簡單分析日誌檔案中的執行次數與狀態"""
        if not os.path.exists(self.log_file):
            return {"total_tasks": 0, "success_rate": "100%"}

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                total = len(lines)
                success_count = sum(1 for line in lines if "SUCCESS" in line)
                rate = (success_count / total * 100) if total > 0 else 100
                return {
                    "total_tasks": total,
                    "success_rate": f"{rate:.1f}%"
                }
        except Exception as e:
            print(f"-> ⚠️ [分析外掛] 讀取日誌分析失敗: {e}")
            return {"total_tasks": 0, "success_rate": "0%"}

if __name__ == "__main__":
    analytics = AnalyticsPlugin()
    print("System Stats:", analytics.analyze_stats())
