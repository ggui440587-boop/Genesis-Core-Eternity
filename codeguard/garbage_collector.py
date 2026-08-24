import os
import time

# ==============================================================
# System Garbage Collector Module - 系統自動化垃圾回收與清理模組
# ==============================================================

TARGET_EXTENSIONS = [".log", ".tmp"]
MAX_FILE_AGE_SECONDS = 86400  # 預設保留一天 (24小時)，超過則清理

class SystemGarbageCollector:
    @staticmethod
    def sweep_debris(directory="."):
        """掃描並清理目錄中的過期暫存與日誌檔"""
        print("=" * 60)
        print(" 🧹 [垃圾回收] 開始掃描系統內部環境與暫存檔案...")
        print("=" * 60)

        cleaned_count = 0
        current_time = time.time()

        for filename in os.listdir(directory):
            # 檢查是否為目標清理副檔名
            if any(filename.endswith(ext) for ext in TARGET_EXTENSIONS):
                file_path = os.path.join(directory, filename)
                file_mtime = os.path.getmtime(file_path)
                file_age = current_time - file_mtime

                # 如果檔案超過保存期限，則進行清理
                if file_age > MAX_FILE_AGE_SECONDS:
                    try:
                        os.remove(file_path)
                        print(f"[清理成功] 已移除過期檔案: [{filename}] (存放超過 {int(file_age // 3600)} 小時)")
                        cleaned_count += 1
                    except Exception as e:
                        print(f"[清理失敗] 無法移除檔案 [{filename}]: {e}")

        print(f"-> [回收完畢] 本次共清理了 {cleaned_count} 個過期暫存檔案。")

if __name__ == "__main__":
    SystemGarbageCollector.sweep_debris()

