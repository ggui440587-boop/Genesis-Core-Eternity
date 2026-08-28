import time
import functools

def benchmark(func):
    """用來測量函式執行時間的效能基準測試裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"-> ⏱️ [效能基準] 函式 '{func.__name__}' 執行耗時: {elapsed_time:.6f} 秒")
        return result
    return wrapper

if __name__ == "__main__":
    @benchmark
    def heavy_computation_task():
        """模擬一段耗時的計算任務"""
        total = sum(i for i in range(1000000))
        return total

    print("-> 🚀 開始執行效能測試...")
    heavy_computation_task()
