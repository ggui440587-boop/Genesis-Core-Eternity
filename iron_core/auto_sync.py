import os
import subprocess
from datetime import datetime

def git_auto_sync():
    print("[SYNC] 正在檢查 Git 狀態並準備同步至雲端...")
    
    # 檢查是否為 git 倉庫
    if not os.path.exists(".git"):
        print("[INFO] 初始化本地 Git 倉庫...")
        os.system("git init")
        os.system("git branch -M main")
    
    # 加入所有更新檔案 (包含資料庫與日誌)
    os.system("git add fusion_hub.db brain_execution.log main.py view_db.py")
    
    # 建立帶時間戳記的提交訊息
    commit_msg = f"Auto-sync iron_core state: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    commit_code = os.system(f'git commit -m "{commit_msg}"')
    
    if commit_code == 0:
        print("[SUCCESS] 本地提交成功！")
        # 推送到遠端 (需確保已設定 git remote add origin 你的倉庫網址)
        push_code = os.system("git push origin main")
        if push_code == 0:
            print("[SUCCESS] 成功將最新大腦狀態同步至 GitHub 雲端！")
        else:
            print("[WARNING] 推送至遠端失敗，請確認是否已設定遠端倉庫與 Token 認證。")
    else:
        print("[INFO] 沒有偵測到需要變更的新資料。")

if __name__ == "__main__":
    git_auto_sync()
