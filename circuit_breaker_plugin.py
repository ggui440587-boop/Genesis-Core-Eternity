import time

class CircuitBreakerPlugin:
    def __init__(self, failure_threshold=3, recovery_timeout=5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"  # 狀態: CLOSED (正常), OPEN (斷開), HALF-OPEN (半開)
        self.last_failure_time = 0
        print("-> 🔌 [斷路器外掛] 容錯保護系統初始化成功！")

    def call(self, func, *args, **kwargs):
        """透過斷路器安全執行指定的函式"""
        now = time.time()
        
        # 如果處於 OPEN 狀態，檢查是否過了恢復時間
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                print("-> 🔌 [斷路器外掛] 進入半開狀態 (HALF-OPEN)，正在測試恢復...")
            else:
                print("-> ⚠️ [斷路器外掛] 電路處於斷開狀態 (OPEN)，拒絕執行以保護系統！")
                return None

        try:
            result = func(*args, **kwargs)
            # 執行成功，重置狀態
            if self.state in ["HALF-OPEN", "OPEN"]:
                print("-> ✅ [斷路器外掛] 系統已成功恢復，電路重新閉合 (CLOSED)。")
            self.state = "CLOSED"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = now
            print(f"-> ❌ [斷路器外掛] 執行失敗 (累計錯誤: {self.failure_count}): {e}")
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("-> 🛑 [斷路器外掛] 錯誤次數達上限，電路已切斷 (OPEN)！")
            raise e

if __name__ == "__main__":
    cb = CircuitBreakerPlugin(failure_threshold=2, recovery_timeout=2)
    
    def unstable_task():
        raise RuntimeError("Network Timeout")

    for i in range(3):
        try:
            cb.call(unstable_task)
        except:
            pass
        time.sleep(0.5)
