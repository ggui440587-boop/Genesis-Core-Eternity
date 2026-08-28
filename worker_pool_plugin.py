from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class WorkerPoolPlugin:
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        print(f"-> 🧵 [執行緒池外掛] 執行緒安全派發器初始化成功 (最大執行緒數: {max_workers})")

    def run_tasks(self, task_func, items):
        """將多個項目分發到執行緒池中並行處理"""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任務
            future_to_item = {executor.submit(task_func, item): item for item in items}
            
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    print(f"-> ❌ [執行緒池錯誤] 項目 '{item}' 執行失敗: {e}")
        return results

if __name__ == "__main__":
    pool = WorkerPoolPlugin(max_workers=2)
    
    def mock_download_task(name):
        print(f"-> 📥 開始處理: {name}")
        time.sleep(0.5)
        return f"{name} 完成"

    items_to_process = ["檔案A", "檔案B", "檔案C", "檔案D"]
    print("-> 🚀 啟動並行任務派發...")
    outputs = pool.run_tasks(mock_download_task, items_to_process)
    print("Task Results:", outputs)
