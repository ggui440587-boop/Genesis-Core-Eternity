import os
import subprocess
from datetime import datetime

def git_backup():
    print("[BACKUP] 正在準備將本地資料庫同步至 GitHub...")
    # 確保設定了 Git 身分與遠端
    os.system("git add fusion_hub.db")
    commit_msg = f"Auto-backup database: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    os.system(f'git commit -m "{commit_msg}"')
    
    # 推送到遠端 (假設你已經設定好 git remote push)
    exit_code = os.system("git push origin main")
    if exit_code == 0:
        print("[SUCCESS] 資料庫雲端備份成功！")
    else:
        print("[WARNING] 備份推送失敗，請確認是否已設定好 GitHub Git 認證。")

if __name__ == "__main__":
    git_backup()
