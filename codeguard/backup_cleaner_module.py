import os
import shutil
import datetime

class BackupCleanerModule:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"-> 📦 [Backup] 開始執行資料庫與日誌備份...")

        # 備份資料庫
        if os.path.exists("fusion_hub.db"):
            dest_db = os.path.join(self.backup_dir, f"fusion_hub_{timestamp}.db")
            shutil.copy("fusion_hub.db", dest_db)
            print(f"   [✓] 資料庫已成功備份至: {dest_db}")

        # 備份日誌
        if os.path.exists("genesis_system.log"):
            dest_log = os.path.join(self.backup_dir, f"genesis_system_{timestamp}.log")
            shutil.copy("genesis_system.log", dest_log)
            print(f"   [✓] 系統日誌已成功備份至: {dest_log}")

if __name__ == "__main__":
    backup_module = BackupCleanerModule()
    backup_module.create_backup()

