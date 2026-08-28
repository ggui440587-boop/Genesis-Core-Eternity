class AgentCoordinatorPlugin:
    def __init__(self):
        self.agents = {}
        print("-> 🤖 [Agent 協調外掛] 多 Agent 團隊管理系統初始化成功！")

    def register_agent(self, role_name, callback_func):
        """註冊特定角色的 Agent 及其處理邏輯"""
        self.agents[role_name] = callback_func
        print(f"-> 👤 [Agent 協調] 已成功納入團隊角色: {role_name}")

    def dispatch_task(self, role_name, task_data):
        """將任務分派給指定的 Agent 角色"""
        if role_name not in self.agents:
            print(f"-> ❌ [Agent 協調錯誤] 找不到角色: {role_name}")
            return None
        
        print(f"-> 🚀 [Agent 協調] 正在將任務指派給 '{role_name}'...")
        agent_func = self.agents[role_name]
        return agent_func(task_data)

if __name__ == "__main__":
    coordinator = AgentCoordinatorPlugin()
    
    # 註冊工程部門 Agent
    coordinator.register_agent("Engineering", lambda task: f"工程團隊已完成代碼編寫: {task}")
    # 註冊研究部門 Agent
    coordinator.register_agent("Research", lambda task: f"研究團隊已完成數據分析: {task}")

    # 測試任務分派
    print(coordinator.dispatch_task("Engineering", "模組化重構專案"))
    print(coordinator.dispatch_task("Research", "AI 模型效能評估"))
