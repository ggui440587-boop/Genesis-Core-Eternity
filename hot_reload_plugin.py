import os

class HotReloadPlugin:
    def __init__(self, config_filename="config.json"):
        self.config_filename = config_filename
        self.last_mtime = self._get_mtime()
        print(f"-> 🔄 [熱重載外掛] 初始化成功，正在監控檔案: {config_filename}")

    def _get_mtime(self):
        """取得檔案的最後修改時間戳記"""
        if os.path.exists(self.config_filename):
            return os.path.getmtime(self.config_filename)
        return 0

    def check_reload_needed(self):
        """檢查設定檔是否有被修改過"""
        current_mtime = self._get_mtime()
        if current_mtime != self.last_mtime:
            self.last_mtime = current_mtime
            print("-> 🔄 [熱重載外掛] 偵測到設定檔已更新，準備重新載入參數！")
            return True
        return False

if __name__ == "__main__":
    watcher = HotReloadPlugin()
    watcher.check_reload_needed()
