from concurrent.futures import ThreadPoolExecutor
import time

class ThreadPoolPlugin:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        print(f"-> 🧵 [執行緒池外掛] 初始化成功，最大並行工作數: {max_workers}")

    def run_concurrent_task(self, task_name, delay=1):
        """提交一項並行背景任務至執行緒池"""
        def background_job():
            time.sleep(delay)
            return f"Task {task_name} completed."
        
        future = self.executor.submit(background_job)
        return future

if __name__ == "__main__":
    pool = ThreadPoolPlugin(max_workers=2)
    f = pool.run_concurrent_task("Test-A", 1)
    print("Result:", f.result())
