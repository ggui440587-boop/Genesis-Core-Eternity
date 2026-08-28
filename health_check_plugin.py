import time

class HealthCheckPlugin:
    def __init__(self):
        self.services = {}
        print("-> 💓 [健康檢查外掛] 自我修復與狀態監控系統初始化成功！")

    def register_service(self, name, check_func):
        """註冊需要健康檢查的服務或模組"""
        self.services[name] = check_func
        print(f"-> 💓 [健康檢查外掛] 已成功註冊監控服務: {name}")

    def run_checks(self):
        """執行所有註冊服務的健康檢查"""
        print("-> 🔍 [健康檢查外掛] 開始進行全系統健康掃描...")
        for name, check_func in self.services.items():
            try:
                status = check_func()
                if status:
                    print(f"-> ✅ [健康檢查] 服務 '{name}' 狀態: 正常 (Healthy)")
                else:
                    print(f"-> ⚠️ [健康檢查] 服務 '{name}' 狀態: 異常，準備觸發修復！")
            except Exception as e:
                print(f"-> ❌ [健康檢查] 服務 '{name}' 檢測發生錯誤: {e}")

if __name__ == "__main__":
    checker = HealthCheckPlugin()
    
    # 註冊一個模擬的正常服務
    checker.register_service("DatabaseService", lambda: True)
    checker.run_checks()
