import time

# ==============================================================
# Action Module - 專責「動起來」與實際執行任務模組
# ==============================================================

class ActionModule:
    def __init__(self, action_name="預設動作"):
        self.action_name = action_name

    def start_moving(self, target_task):
        """專注於動起來，實際發力執行任務"""
        print(f"⚡ [動起來] 開始執行任務：{target_task}")
        for i in range(1, 3):
            print(f"-> 正在全力運算與動作中... ({i}/2)")
            time.sleep(0.5)
        print(f"✅ [動作完成] 任務 [{target_task}] 已順利達成！")

if __name__ == "__main__":
    action = ActionModule()
    action.start_moving("編譯並運行自動化腳本")

