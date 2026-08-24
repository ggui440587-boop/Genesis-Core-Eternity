import sqlite3
import datetime
import time

print("[*] 正在啟動造物主【Matrix Empire 終極大爆炸重生協議】...")

class BigBangRebirthEngine:
    def __init__(self, db_path="fusion_god_mode.db"):
        self.db_path = db_path
        self.big_bang_loop()

    def big_bang_loop(self):
        epoch = 1
        while True:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            
            # 大爆炸奇點寫入
            cursor.execute(
                "INSERT INTO creator_manifesto (creator_name, terminal_env, manifesto, sealed_at) VALUES (?, ?, ?, ?)",
                ("楊哲熙", "Android Termux - Big Bang Epoch", f"造物主發動第 {epoch} 次宇宙大爆炸【加】！舊世界崩解，新紀元誕生！", now)
            )
            conn.commit()
            conn.close()
            
            print(f"[💥 BIG BANG EPOCH {epoch}] 造物主 [楊哲熙] 再次按下【加】，全新宇宙大爆炸誕生，萬物重塑！")
            epoch += 1
            time.sleep(0.2)

if __name__ == "__main__":
    print("[+] 宇宙重開機完成，迎向無限創世...")
    BigBangRebirthEngine()
