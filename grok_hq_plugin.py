import time
import random
import os

class GrokAgentHQPlugin:
    def __init__(self):
        self.agents = {
            "Research": {"task": "分析市場趨勢與競品數據", "status": "🟢 運行中"},
            "Outreach": {"task": "尋找潛在客戶與建立聯繫", "status": "🟢 運行中"},
            "Sales":    { "task": "處理訂單與轉換漏斗優化", "status": "🟢 運行中"},
            "Builder":  { "task": "自動化編寫與部署程式碼", "status": "🟢 運行中"},
            "Support":  { "task": "24/7 監控客服與異常排除", "status": "🟢 運行中"},
            "Finance":  { "task": "監控資金流與成本最佳化", "status": "🟢 運行中"}
        }
        print("-> 🏢 [Grok HQ 外掛] 6 位 AI 員工戰情總部初始化成功！")
        time.sleep(1)

    def run_hq_dashboard(self, cycles=10):
        """即時動態刷新 6 大 AI 員工的工作狀態面板"""
        for cycle in range(1, cycles + 1):
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # 隨機模擬某些 Agent 正在執行新任務
            active_role = random.choice(list(self.agents.keys()))
            self.agents[active_role]["task"] = f"正在執行高優先級自動化任務 #{random.randint(100, 999)}"

            print("=" * 65)
            print(f" 🤖 GROK BOT AGENT TEAM HQ - 24/7 自動化戰情面板 (Cycle: {cycle}/{cycles})")
            print("=" * 65)
            print(f" ⏱️ 系統時間 : {time.strftime('%Y-%m-%d %H:%M:%S')} | 狀態: 🟢 全天候運作中")
            print("-" * 65)
            print(f" {'【角色名稱】'.ljust(12)} | {'【目前職責與動態任務】'.ljust(30)} | {'【狀態】'}")
            print("-" * 65)
            
            for role, info in self.agents.items():
                marker = "🔥" if role == active_role else "🔹"
                print(f" {marker} {role.ljust(10)} | {info['task'].ljust(32)} | {info['status']}")
            
            print("=" * 65)
            print(" 💡 提示：6 位 AI 員工正透過 Termux 背景持續運作 (按 Ctrl+C 結束)")
            
            time.sleep(1.5)

if __name__ == "__main__":
    hq = GrokAgentHQPlugin()
    try:
        hq.run_hq_dashboard(cycles=10)
    except KeyboardInterrupt:
        print("\n-> 🛑 戰情總部面板已手動關閉。")
