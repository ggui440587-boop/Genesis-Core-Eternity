class DatabasePlugin:
    def save_log(self, task_id, status):
        print(f"-> 💾 [資料庫] 記錄任務 #{task_id} 狀態: {status}")
