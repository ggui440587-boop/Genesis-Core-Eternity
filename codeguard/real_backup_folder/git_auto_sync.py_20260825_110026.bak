import subprocess
import datetime

# ==============================================================
# Git Auto Sync Module - 程式碼自動化遠端同步與推送模組
# ==============================================================

class GitAutoSync:
    @staticmethod
    def sync_repository():
        print("=" * 60)
        print(" 🔄 [Git 自動同步] 開始檢查並推送累積的專案進度...")
        print("=" * 60)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-sync ecosystem code at {timestamp}"

        try:
            # 1. 嘗試將當前變更加入暫存並提交
            subprocess.run(["git", "add", "*.py", "*.json", "*.sh"], capture_output=True)
            commit_result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)

            if commit_result.returncode == 0:
                print(f"-> 🟢 成功建立新提交: {commit_message}")
            else:
                print("-> ℹ️ 目前無新變更需要提交，準備直接推送已累積的 commits。")

            # 2. 強制執行遠端推送 (Push)
            print("-> 🚀 正在將最新程式碼推送到遠端 GitHub 儲存庫...")
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("-> 🎉 成功！所有程式碼已完整同步至 GitHub！")

        except subprocess.CalledProcessError as e:
            print(f"-> 🔴 Git 推送過程發生錯誤，請確認網路與權杖設定: {e}")

        print("=" * 60)

if __name__ == "__main__":
    GitAutoSync.sync_repository()

