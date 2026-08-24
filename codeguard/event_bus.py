# ==============================================================
# System Event Bus - 系統神經訊息匯流排與反射弧模組
# ==============================================================

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback_func):
        """訂閱某個類型的系統事件（如：心跳、感知、肌肉施力）"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback_func)
        print(f"[神經匯流排] 成功註冊事件監聽: [{event_type}]")

    def publish(self, event_type, data):
        """發布事件，通知所有訂閱的模組進行相應動作（反射弧）"""
        print(f"[神經脈衝] ⚡ 觸發事件 [{event_type}] 帶有資料: {data}")
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

# 測試回呼函式（模擬身體各部位的反應）
def brain_reaction(data):
    print(f" -> [大腦接收] 已分析事件內容: {data}")

def muscle_reaction(data):
    print(f" -> [肌肉接收] 準備因應事件進行發力: {data}")

if __name__ == "__main__":
    print("=" * 60)
    print(" ⚡ 系統神經匯流排與反射弧模組啟動")
    print("=" * 60)

    bus = EventBus()
    # 各部位訂閱事件
    bus.subscribe("SYSTEM_ALERT", brain_reaction)
    bus.subscribe("SYSTEM_ALERT", muscle_reaction)

    # 模擬觸發一個緊急系統警報事件
    bus.publish("SYSTEM_ALERT", "偵測到外部環境資料變動，全體警戒！")

