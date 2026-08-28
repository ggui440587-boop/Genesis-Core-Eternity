import datetime
import json

class IntegratedSystem:
    def __init__(self):
        print("-> 🚀 [整合系統] 初始化完成：大腦核心與虛擬傳輸通道已連線。")

    def process_and_dispatch(self, user_command):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-> 📥 [系統接收指令 - {timestamp}] 『{user_command}』")

        # 1. 大腦核心進行語意分析
        if "前進" in user_command or "移動" in user_command:
            action = "MOVE_FORWARD"
            target = "SECTOR_A"
        elif "撤退" in user_command or "危險" in user_command:
            action = "EMERGENCY_RETREAT"
            target = "SAFE_ZONE"
        else:
            action = "START_PATROL"
            target = "PERIMETER"

        # 2. 封裝指令封包
        packet = {
            "timestamp": timestamp,
            "action": action,
            "target": target,
            "status": "DISPATCHED"
        }

        print(f"-> 🧠 [大腦決策] 轉換完成 -> 動作: {action}, 目標: {target}")
        print(f"-> 📡 [網路傳輸] 正在將控制封包發送至虛擬機器人端...")
        print(f"-> [✔] 機器人端回報: 執行成功 ({json.dumps(packet, ensure_ascii=False)})")

if __name__ == "__main__":
    system = IntegratedSystem()

    # 測試整合系統運作
    system.process_and_dispatch("請指揮機器人前往目標區域進行偵查")

