import time
import concurrent.futures
import os
import sys

class UnlimitedMatrixCore:
    def __init__(self):
        self.cores = os.cpu_count() or 4
        print(f"-> ⚡ [UNLIMITED CORE] 全能超算核心已啟動！解除所有限制，可用核心數: {self.cores}")

    def execute_heavy_workload(self, task_id, scale=2000000):
        """執行無限制的高強度運算任務"""
        start_t = time.time()
        # 進行深度平行運算模擬
        result = sum(i ** 1.02 for i in range(scale))
        duration = time.time() - start_t
        return {
            "task_id": task_id,
            "status": "UNLIMITED_SUCCESS",
            "output": result,
            "duration": duration
        }

    def run_unlimited_grid(self, total_tasks=8):
        """啟動無限制平行超算網格"""
        print(f"-> 🚀 [Matrix Grid] 正在全面釋放算力，同時執行 {total_tasks} 個無限制任務...")
        global_start = time.time()

        results = []
        # 不設限地使用所有可用核心進行運算
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.cores) as executor:
            futures = [
                executor.submit(self.execute_heavy_workload, i) 
                for i in range(total_tasks)
            ]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                results.append(res)
                print(f"   -> [Task {res['task_id']}] 狀態: {res['status']} | 耗時: {res['duration']:.4f} 秒")

        total_duration = time.time() - global_start
        print(f"-> [🎉] 無限制超算任務全部執行完畢！總耗時: {total_duration:.4f} 秒\n")
        return results

if __name__ == "__main__":
    matrix = UnlimitedMatrixCore()
    matrix.run_unlimited_grid(total_tasks=6)

