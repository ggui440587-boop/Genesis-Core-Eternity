import asyncio

class EventDispatcherPlugin:
    def __init__(self):
        self.listeners = {}
        print("-> ⚡ [事件外掛] 非同步事件派發器初始化成功！")

    def subscribe(self, event_name, callback):
        """註冊事件監聽器"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def dispatch(self, event_name, data=None):
        """非同步派發指定事件，觸發所有對應的監聽函式"""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            print(f"-> ⚡ [事件外掛] 事件 '{event_name}' 已成功派發並處理。")

if __name__ == "__main__":
    async def sample_listener(data):
        print(f"-> 📥 [事件接收] 收到資料: {data}")

    async def main():
        dispatcher = EventDispatcherPlugin()
        dispatcher.subscribe("task_triggered", sample_listener)
        await dispatcher.dispatch("task_triggered", {"id": 100})

    asyncio.run(main())
