import urllib.request
import json
import time

class CentralAIHub:
    def __init__(self, target_robot_url="http://127.0.0.1:9000"):
        self.target_robot_url = target_robot_url
        print("-> 🌐 [中央 AI 主控台] 初始化完成，準備調度機器人網路。")

    def dispatch_task(self, task_id, command, priority):
        """中央 AI 生成指令並派發給機器人節點"""
        payload = {
            "task_id": task_id,
            "command": command,
            "priority": priority
        }
        data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            self.target_robot_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            print(f"\n-> ⚡ [AI 決策] 正在派發任務 [{task_id}] -> 指令: {command}")
            with urllib.request.urlopen(req, timeout=3) as res:
                result = json.loads(res.read().decode('utf-8'))
                print(f"-> [✔] 機器人節點回報確認: {result}")
        except Exception as e:
            print(f"-> [❌] 指令派發失敗: {e}")

if __name__ == "__main__":
    hub = CentralAIHub()
    # 模擬中央 AI 自動下達實體操作任務
    hub.dispatch_task("TASK-2026-001", "SECURE_PERIMETER_AND_PATROL", priority=5)

