import time
import subprocess
import datetime

class MatrixScheduler:
    def __init__(self, interval_hours=2):
        self.interval_seconds = interval_hours * 3600
        print(f"[Matrix-Scheduler] 正在初始化永動心跳排程網 (心跳頻率: 每 {interval_hours} 小時)...")

    def pulse_heartbeat(self):
        """執行一次完整的帝國作戰循環"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n================================================")
        print(f"🔥 [Matrix Heartbeat] 觸發永動循環！時間: {current_time}")
        print(f"================================================\n")

        # 1. 執行免疫防禦與系統健康檢查
        print("▶ [步驟 1/3] 執行免疫守衛與資料庫健康掃描...")
        subprocess.run("python matrix_vector_immune.py", shell=True)

        # 2. 執行鏈上雷達與情報更新
        print("\n▶ [步驟 2/3] 執行鏈上雷達與智庫情報同步...")
        subprocess.run("python matrix_web3_graph_agent.py", shell=True)

        # 3. 執行加密保險箱封存與自動變現漏斗
        print("\n▶ [步驟 3/3] 執行加密保險箱封存與自動變現分發...")
        subprocess.run("python matrix_monetize_vault.py", shell=True)

        print(f"\n✅ [Matrix Heartbeat] 本輪帝國循環完畢。進入休眠，等待下一次心跳...\n")

    def start_eternal_loop(self):
        """啟動永不停止的背景心跳無限迴圈"""
        print("[⚡ 核心宣告] 矩陣永動機已正式點火！手機將在背景自主運轉。")
        print("（提示：若要終止，請按 Ctrl + C）")
        
        # 確保常駐時保持手機喚醒
        subprocess.run("termux-wake-lock", shell=True)

        try:
            while True:
                self.pulse_heartbeat()
                # 倒數計時等待下一次心跳
                time.sleep(self.interval_seconds)
        except KeyboardInterrupt:
            print("\n[🛑 系統通知] 永動機手動暫停。你的 Termux 帝國隨時可再次喚醒！")

if __name__ == "__main__":
    # 預設每 2 小時一個心跳循環（測試時可以將這裡改小，例如 60 秒）
    scheduler = MatrixScheduler(interval_hours=2)
    scheduler.start_eternal_loop()

