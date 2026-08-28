import time
import functools

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """指數退避重試機制的 Python 裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    sleep_time = backoff_in_seconds * (2 ** x)
                    print(f"-> 🔄 [重試外掛] 執行失敗: {e}。將於 {sleep_time} 秒後進行第 {x + 1} 次重試...")
                    time.sleep(sleep_time)
                    x += 1
            print(f"-> ❌ [重試外掛] 已達最大重試次數 ({retries})，放棄執行。")
            raise RuntimeError("Max retries reached")
        return wrapper
    return decorator

if __name__ == "__main__":
    @retry_with_backoff(retries=3, backoff_in_seconds=0.5)
    def flaky_network_call():
        print("-> 🌐 嘗試連線至外部伺服器...")
        raise ConnectionError("Network Unstable")

    try:
        flaky_network_call()
    except Exception:
        print("-> 🛑 任務最終終止。")
