import concurrent.futures
import time

class ParallelSchedulerModule:
    def __init__(self):
        pass

    def sample_task(self, name, duration):
        print(f"-> ⏳ [Task] 任務 {name} 開始執行...")
        time.sleep(duration)
        print(f"   [✓] 任務 {name} 執行完畢！")
        return f"{name}_SUCCESS"

    def run_parallel_pipeline(self):
        print("-> 🚀 [ParallelScheduler] 啟動多執行緒平行任務管線...")
        tasks = [("NodeJS_Worker", 1), ("C_Optimizer", 1), ("Python_Scraper", 2)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(self.sample_task, name, dur): name for name, dur in tasks}
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                print(f"   [記錄] 收到執行結果: {res}")
        print("   [✓] 所有平行任務已圓滿完成。")

if __name__ == "__main__":
    scheduler = ParallelSchedulerModule()
    scheduler.run_parallel_pipeline()

