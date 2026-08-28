# 全域外掛倉庫
PLUGIN_REGISTRY = {}

def register_plugin(name):
    """用來自動註冊外掛的 Python 裝飾器"""
    def decorator(cls):
        PLUGIN_REGISTRY[name] = cls
        print(f"-> 🪄 [裝飾器外掛] 自動註冊外掛成功: {name}")
        return cls
    return decorator

if __name__ == "__main__":
    @register_plugin("SuperModule")
    class SuperPlugin:
        def run(self):
            print("-> 🚀 超級外掛執行中！")

    # 驗證自動註冊結果
    plugin_instance = PLUGIN_REGISTRY["SuperModule"]()
    plugin_instance.run()
