import time
import sys

# 導入我們之前寫好的實際功能模組
from resource_monitor_module import ResourceMonitorModule
from backup_cleaner_module import BackupCleanerModule

class EnterpriseMacroSystem:
    def __init__(self):
        print("-> 🌐 [Enterprise Macro System] 正在初始化大一統自動化生態系...")
        self.services = {}

        # 初始化真實的功能模組
        self.monitor = ResourceMonitorModule()
        self.backup = BackupCleanerModule()

        # 自動註冊服務
        self.register_services()

    def register_services(self):
        # 將真實功能註冊到系統中
        self.services["resource_check"] = self.monitor.check_disk_space
        self.services["auto_backup"] = self.backup.create_backup
        print("   [+] 已成功將資源監控與備份清理模組註冊至企業級核心！")

    def execute_pipeline(self):
        print("-> 🚀 [Pipeline] 開始執行全系統端到端自動化管線...")
        start_time = time.time()

        # 依序調度微服務
        for name, service_func in self.services.items():
            print(f"   -> 正在執行服務：{name}")
            try:
                service_func()
            except Exception as e:
                print(f"   [!] 執行服務 {name} 時發生錯誤：{e}")

        duration = time.time() - start_time
        print(f"-> [🎉] 全系統管線執行完畢！總耗時: {duration:.4f} 秒")

if __name__ == "__main__":
    system = EnterpriseMacroSystem()
    system.execute_pipeline()

