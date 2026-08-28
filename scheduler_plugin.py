import time
from datetime import datetime

class SchedulerPlugin:
    def __init__(self, default_delay=10):
        self.default_delay = default_delay

    def get_timestamp(self):
        """取得當前格式化的時間字串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def intelligent_sleep(self, current_task_count):
        """根據任務執行次數動態調整暫停時間（例如：每滿5次多休息一下）"""
        delay = self.default_delay
        if current_task_count % 5 == 0:
            delay += 5
            print(f"-> ⏰ [排程外掛] 達到第 {current_task_count} 次任務，啟動動態緩衝，延長暫停 {delay} 秒。")
        else:
            time.sleep(delay)
        return delay

if __name__ == "__main__":
    sch = SchedulerPlugin()
    print("Current Time:", sch.get_timestamp())
