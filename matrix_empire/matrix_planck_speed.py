import sqlite3
import datetime

print("[*] 正在啟動造物主【Matrix Empire 普朗克極速創世協議】...")

class PlanckSpeedEngine:
    def __init__(self, db_path="fusion_god_mode.db"):
        self.db_path = db_path
        self.planck_loop()

    def planck_loop(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 開啟資料庫極速記憶體Journal模式
        cursor.execute("PRAGMA journal_mode = MEMORY;")
        cursor.execute("PRAGMA synchronous = OFF;")
        
        batch_count = 1
        print("[⚡ PLANCK] 普朗克時間加速器已啟動，開始每秒數千筆造物主神諭灌入！按 Ctrl+C 停止。")
        
        try:
            while True:
                now = datetime.datetime.now().isoformat()
                # 批量建構資料
                data_batch = [
                    ("楊哲熙", "Android Termux - Planck Speed", f"造物主發動第 {batch_count * i} 次普朗克【加】！時空微觀結構重組中...", now)
                    for i in range(1, 101)
                ]
                cursor.executemany(
                    "INSERT INTO creator_manifesto (creator_name, terminal_env, manifesto, sealed_at) VALUES (?, ?, ?, ?)",
                    data_batch
                )
                conn.commit()
                print(f"[🌌 PLANCK BATCH {batch_count}] 造物主 [楊哲熙] 的意志已瞬間灌入 100 筆微觀矩陣數據！")
                batch_count += 1
        except KeyboardInterrupt:
            conn.close()
            print("\n[+] 普朗克加速暫停，造物主掌控永恆。")

if __name__ == "__main__":
    PlanckSpeedEngine()
