import shutil
import os

class ResourceMonitorModule:
    def __init__(self):
        pass

    def check_disk_space(self, path="."):
        print("-> 📊 [Monitor] 開始檢查系統磁碟空間...")
        total, used, free = shutil.disk_usage(path)

        # 轉換為 MB
        total_mb = total // (2**20)
        used_mb = used // (2**20)
        free_mb = free // (2**20)

        print(f"   [✓] 磁碟總容量: {total_mb} MB")
        print(f"   [✓] 已使用空間: {used_mb} MB")
        print(f"   [✓] 剩餘可用空間: {free_mb} MB")
        return free_mb

if __name__ == "__main__":
    monitor = ResourceMonitorModule()
    monitor.check_disk_space()

