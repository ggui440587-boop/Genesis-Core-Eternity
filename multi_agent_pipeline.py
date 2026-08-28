import datetime

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def execute(self, task_data):
        print(f"-> 🤖 代理人 [{self.name}] ({self.role}) 正在處理任務...")
        # 模擬代理人執行過程
        result = f"[{self.name} 執行結果] 已成功處理資料: {task_data}"
        return result

class MultiAgentOrchestrator:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def run_pipeline(self, initial_input):
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> 🚀 啟動多代理人協作管線...")
        current_data = initial_input
        
        for agent in self.agents:
            current_data = agent.execute(current_data)
            print(f"-> ✅ {agent.name} 完成階段性目標。\n")
            
        print(f"-> 🎉 最終結算成果:\n{current_data}")

if __name__ == "__main__":
    # 1. 建立總指揮官
    orchestrator = MultiAgentOrchestrator()

    # 2. 註冊多個代理人
    orchestrator.add_agent(Agent("Grok-Agent", "數據檢索與過濾"))
    orchestrator.add_agent(Agent("Kimi-Agent", "邏輯分析與合成"))

    # 3. 啟動管線
    orchestrator.run_pipeline("原始開源專案清單與程式碼片段")
