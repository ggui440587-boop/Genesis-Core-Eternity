import datetime

class HeartbeatModule:
    def __init__(self):
        pass

    def send_heartbeat(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"-> 💓 [Heartbeat] 系統心跳正常：當前運作中 ({timestamp})")
        return timestamp

if __name__ == "__main__":
    heartbeat = HeartbeatModule()
    heartbeat.send_heartbeat()

