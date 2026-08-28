import os

class EnvPlugin:
    def __init__(self):
        print("-> 🔐 [憑證外掛] 環境變數與安全金鑰管理器初始化成功！")

    def get_env(self, key, default=None):
        """安全地取得環境變數，若不存在則回傳預設值"""
        value = os.environ.get(key, default)
        if value is None:
            print(f"-> ⚠️ [憑證外掛] 警告: 未找到環境變數 '{key}'")
        return value

if __name__ == "__main__":
    env = EnvPlugin()
    # 測試讀取一個常見的系統變數
    print("Termux User:", env.get_env("USER", "Unknown"))
