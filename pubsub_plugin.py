class MessageBusPlugin:
    def __init__(self):
        self.subscribers = {}
        print("-> 📯 [訊息匯流排外掛] Pub/Sub 系統初始化成功！")

    def subscribe(self, topic, callback):
        """訂閱指定的訊息主題"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        print(f"-> 📯 [訊息匯流排] 成功訂閱主題: {topic}")

    def publish(self, topic, message):
        """向指定主題發布訊息，所有訂閱者都會收到"""
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)
            print(f"-> 📯 [訊息匯流排] 主題 '{topic}' 已廣播訊息。")

if __name__ == "__main__":
    bus = MessageBusPlugin()
    
    def my_listener(msg):
        print(f"-> 📥 [收到廣播] 內容: {msg}")

    bus.subscribe("system_alerts", my_listener)
    bus.publish("system_alerts", "CPU 負載過高警報！")
