import os
import time
import subprocess

class MatrixCronGuard:
    def __init__(self, name="Termux-Matrix-Guard"):
        self.name = name
        print(f"[{self.name}] 守衛與自動排程中樞已啟動...")

    def check_and_revive_processes(self):
        """檢查主雷達是否仍在背景運行，若掛掉則自動復活"""
        cmd = "ps aux | grep web3_code_matrix.py"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # 如果除了 grep 之外找不到其他行程，代表主雷達當掉了
        lines = [line for line in result.stdout.split('\n') if 'grep' not in line and line.strip()]
        
        if not lines:
            print(f"[{self.name}] 警報：主雷達失聯！正在自動重啟主雷達...")
            subprocess.Popen("nohup python web3_code_matrix.py > matrix_code_run.log 2>&1 &", shell=True)
        else:
            print(f"[{self.name}] 主雷達運行狀態：正常 (Healthy)")

    def run_daily_pipeline(self):
        """執行全套流水線：深度挖掘 ➔ 更新資料庫 ➔ 生成短影音與文章腳本"""
        print(f"[{self.name}] 正在執行全自動情報煉金術（深度挖掘 + 工廠產出）...")
        try:
            # 1. 執行深度挖掘與過濾
            subprocess.run(["python", "deep_diver.py"], check=True)
            # 2. 執行智庫入庫與腳本自動生成
            subprocess.run(["python", "matrix_factory.py"], check=True)
            print(f"[{self.name}] 全自動煉金完畢！最新情報與腳本已產出。")
        except Exception as e:
            print(f"[{self.name}] 煉金流水線執行時發生異常: {e}")

    def start_guardian_loop(self):
        """全天候守衛迴圈：每隔 1 小時檢查主雷達，每隔 4 小時執行一次自動煉金"""
        counter = 0
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n--- [{timestamp}] 矩陣守衛進行例行巡檢 ---")
            
            # 檢查主雷達
            self.check_and_revive_processes()
            
            # 每 4 小時（4次循環）執行一次全套情報煉金
            if counter % 4 == 0:
                self.run_daily_pipeline()
            
            counter += 1
            # 每小時巡檢一次
            time.sleep(3600)

if __name__ == "__main__":
    guard = MatrixCronGuard()
    guard.start_guardian_loop()

