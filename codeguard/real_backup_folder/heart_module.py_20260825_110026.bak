import time
import datetime

# ==============================================================
# System Heart Module - 系統心臟與動力源模組 (象徵軀幹與能量循環)
# ==============================================================

class SystemHeart:
    def __init__(self, heart_rate=5):
        self.heart_rate = heart_rate  # 心跳間隔秒數
        self.is_beating = True

    def beat(self):
        """模擬心臟規律跳動，提供系統持續運轉的動力"""
        print("=" * 50)
        print(" ❤️ 系統心臟啟動：動力循環中樞開始運作...")
        print("=" * 50)

        try:
            counter = 1
            while self.is_beating:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[第 {counter} 次心跳] 時間: {current_time} | 狀態: 系統動力穩定，各部位運作正常。")
                counter += 1
                time.sleep(self.heart_rate)
        except KeyboardInterrupt:
            print("\n[心臟停止] 收到中斷訊號，動力循環安全關閉。")

if __name__ == "__main__":
    heart = SystemHeart(heart_rate=3)
    heart.beat()

