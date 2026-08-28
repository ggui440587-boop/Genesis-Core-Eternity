class ServiceContainer:
    def __init__(self):
        self._services = {}
        print("-> 🧩 [容器外掛] 依賴注入服務容器初始化成功！")

    def bind(self, name, instance):
        """將指定的服務或外掛實例註冊到容器中"""
        self._services[name] = instance
        print(f"-> 🧩 [容器外掛] 已成功註冊服務: {name}")

    def get(self, name):
        """從容器中取得對應的服務實例"""
        if name not in self._services:
            raise KeyError(f"-> ❌ [容器外掛] 找不到已註冊的服務: {name}")
        return self._services[name]

if __name__ == "__main__":
    container = ServiceContainer()
    container.bind("sample_service", "Hello DI World")
    print("Resolved Service:", container.get("sample_service"))
