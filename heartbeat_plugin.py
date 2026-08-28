import time
class HeartbeatPlugin:
    def __init__(self): self.count = 0
    def pulse(self):
        self.count += 1
        print(f"-> 💓 [心跳] 系統心跳 #{self.count}")
        return self.count
