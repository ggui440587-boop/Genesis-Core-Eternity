import os
import glob

class CacheCleanerPlugin:
    def __init__(self, target_pattern="*.tmp"):
        self.target_pattern = target_pattern

    def clean_cache(self):
        """自動清理專案目錄下的暫存檔案"""
        try:
            files = glob.glob(self.target_pattern)
            count = len(files)
            for f in files:
                os.remove(f)
            if count > 0:
                print(f"-> 🧹 [快取外掛] 已成功清除 {count個} 個暫存檔案。")
            else:
                print("-> 🧹 [快取外掛] 目前沒有發現需要清理的暫存檔案。")
            return count
        except Exception as e:
            print(f"-> ⚠️ [快取外掛] 清理快取失敗: {e}")
            return 0

if __name__ == "__main__":
    cleaner = CacheCleanerPlugin()
    cleaner.clean_cache()
