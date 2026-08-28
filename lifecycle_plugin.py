class LifecyclePluginManager:
    def __init__(self):
        self.plugins = {}
        print("-> 🏭 [生命週期工廠] 外掛管理系統初始化成功！")

    def register(self, name, plugin_instance):
        """註冊外掛並呼叫初始化鉤子"""
        self.plugins[name] = plugin_instance
        if hasattr(plugin_instance, "on_load"):
            plugin_instance.on_load()
        print(f"-> 📦 [生命週期] 外掛 '{name}' 已成功註冊並載入。")

    def start_all(self):
        """啟動所有已註冊的外掛"""
        print("-> 🚀 [生命週期] 正在依序啟動所有模組...")
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "on_start"):
                plugin.on_start()

if __name__ == "__main__":
    class DummyPlugin:
        def on_load(self):
            print("  -> [Dummy] 正在載入...")
        def on_start(self):
            print("  -> [Dummy] 正在啟動...")

    manager = LifecyclePluginManager()
    manager.register("Dummy", DummyPlugin())
    manager.start_all()
