from abc import ABC, abstractmethod

class BasePluginTemplate(ABC):
    def __init__(self, name):
        self.name = name

    def execute_workflow(self):
        """定義標準的執行流程，消除重複的初始化與結構宣告 (Template Method Pattern)"""
        self.log_step("1. 瞭解要求與初始化")
        self.log_step("2. 執行核心邏輯")
        self.run_core_logic()
        self.log_step("3. 執行完畢與收尾")

    def log_step(self, message):
        print(f"-> 🧩 [{self.name}] {message}")

    @abstractmethod
    def run_core_logic(self):
        """由子類別實作各自獨有的核心程式碼，實現程式碼複用"""
        pass

if __name__ == "__main__":
    class ConcreteAgentPlugin(BasePluginTemplate):
        def run_core_logic(self):
            print("  -> 🚀 正在執行專屬的 Agent 任務分派邏輯...")

    plugin = ConcreteAgentPlugin("AgentSystem")
    plugin.execute_workflow()
