import os
import shutil
from datetime import datetime

class RealFileManager:
    def __init__(self, target_dir="./"):
        self.target_dir = os.path.abspath(target_dir)
        self.backup_dir = os.path.join(self.target_dir, "real_backup_folder")
        print(f"-> [真實執行] 目標工作目錄: {self.target_dir}")

    def scan_and_backup_files(self, extension=".py"):
        """掃描並備份真實存在於目錄中的指定副檔名檔案"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            print(f"-> [建立備份夾] 已建立真實備份目錄: {self.backup_dir}")

        files = os.listdir(self.target_dir)
        matched_files = [f for f in files if f.endswith(extension) and f != os.path.basename(__file__)]

        if not matched_files:
            print(f"-> [提示] 在目錄中沒有找到任何副檔為 {extension} 的真實檔案。")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        count = 0

        for file_name in matched_files:
            src_path = os.path.join(self.target_dir, file_name)
            dest_name = f"{file_name}_{timestamp}.bak"
            dest_path = os.path.join(self.backup_dir, dest_name)

            # 執行真實的檔案複製與備份
            shutil.copy2(src_path, dest_path)
            print(f"-> [真實備份成功] {file_name} -> {dest_path}")
            count += 1

        print(f"-> [完成] 總共備份了 {count} 個真實檔案！\n")

if __name__ == "__main__":
    manager = RealFileManager()
    # 執行真實備份當前目錄下的所有 .py 程式碼檔案
    manager.scan_and_backup_files(extension=".py")

