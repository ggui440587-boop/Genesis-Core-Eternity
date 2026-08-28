import datetime
import json

class SmartBrainCore:
    def __init__(self):
        print("-> 🧠 [智慧大腦核心] 初始化完成：已載入高效率本地指令解析模組。")

    def analyze_and_command(self, user_input):
        """大腦對接收到的自然語言進行深度分析與風險評估"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-> 📥 [接收命令 - {timestamp}] 『{user_input}』")

        # 智慧語意分析與邏輯轉換
        action = "IDLE"
        target = "UNKNOWN"
        risk_level = "LOW"

        if "前進" in user_input or "移動" in user_input:
            action = "MOVE_FORWARD"
            target = "VIRTUAL_SECTOR_A"
            risk_level = "MODERATE"
        elif "巡邏" in user_input:
            action = "START_PATROL"
            target = "PERIMETER"
            risk_level = "LOW"
        elif "危險" in user_input or "撤退" in user_input:
            action = "EMERGENCY_RETREAT"
            target = "SAFE_ZONE"
            risk_level = "HIGH"
        else:
            action = "SYSTEM_DIAGNOSTIC"
            target = "SELF_CHECK"
            risk_level = "LOW"

        # 產生結構化機器人控制封包
        command_packet = {
            "timestamp": timestamp,
            "action": action,
            "target": target,
            "risk_assessment": risk_level,
            "status": "READY_TO_DISPATCH"
        }

        print(f"-> ⚡ [大腦決策分析結果]:")
        print(f"   ├─ 目標動作: {action}")
        print(f"   ├─ 目標位置: {target}")
        print(f"   └─ 風險等級: {risk_level}")

        return json.dumps(command_packet, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    brain = SmartBrainCore()

    # 模擬測試多種不同的使用者命令
    test_commands = [
        "請命令機器人前往sector A前進",
        "周遭似乎有狀況，請執行緊急撤退",
        "開始進行全區巡邏"
    ]

    for cmd in test_commands:
        brain.analyze_and_command(cmd)
        print("-" * 40)

