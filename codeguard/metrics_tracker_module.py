import time
import json
import os

class MetricsTrackerModule:
    def __init__(self, metrics_file="genesis_metrics.json"):
        self.metrics_file = metrics_file

    def record_metric(self, task_name, duration_seconds):
        print(f"-> 📈 [Metrics] 記錄任務效能 [{task_name}]: 耗時 {duration_seconds:.4f} 秒")
        data = []
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = []

        data.append({"task": task_name, "duration": duration_seconds, "timestamp": time.time()})

        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    tracker = MetricsTrackerModule()
    start_time = time.time()
    time.sleep(0.5) # 模擬任務執行
    duration = time.time() - start_time
    tracker.record_metric("Sample_Task", duration)

