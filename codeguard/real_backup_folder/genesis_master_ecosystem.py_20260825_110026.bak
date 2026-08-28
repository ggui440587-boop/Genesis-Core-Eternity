# ==============================================================
# Genesis Master Ecosystem - 全系統生態系大一統主控串聯腳本
# ==============================================================

from study_module import StudyModule
from action_module import ActionModule
from knowledge_executor import KnowledgeExecutor
from security_firewall import SecurityFirewall
from zero_day_pathogen_detector import ZeroDayPathogenDetector
from system_psychology_module import SystemPsychologyModule
from system_trauma_module import SystemTraumaHandler
from system_healing_module import SystemHealingModule

class GenesisMasterEcosystem:
    def __init__(self):
        self.study = StudyModule()
        self.executor = KnowledgeExecutor()
        self.action = ActionModule()
        self.psychology = SystemPsychologyModule()

    def run_full_lifecycle(self, command_tag, payload):
        print("=" * 65)
        print(f" 🚀 [主控生態系] 啟動全模組串聯生命週期管線...")
        print("=" * 65)

        # 1. 檢測零時差新型病原體與安全防火牆
        pathogen_status = ZeroDayPathogenDetector.scan_and_quarantine_pathogen(payload)
        if pathogen_status == "QUARANTINED":
            print("-> 🔴 [防禦攔截] 偵測到新型威脅，生態系進入高度隔離狀態，中止本次管線。")
            return

        is_allowed = SecurityFirewall.inspect_request(command_tag)
        if not is_allowed:
            print("-> 🔴 [權限攔截] 請求遭拒，管線中止。")
            return

        # 2. 評估心境與系統環境狀態
        self.psychology.evaluate_mood_and_environment(external_load=45)
        self.psychology.check_system_dysregulation()

        print("-" * 65)

        # 3. 執行「讀書」與知識吸收
        print("📖 [階段一] 執行讀書模組...")
        self.study.read_and_absorb(
            topic="全生態系模組化整合", 
            content="成功將安全防護、心境調節、病原檢測與讀書動作完美串聯。"
        )

        print("-" * 65)

        # 4. 執行「動起來」與知識轉化實作（加入創傷與修復容錯保護）
        print("⚡ [階段二] 執行知識轉化與動作模組...")
        try:
            self.executor.execute_latest_knowledge()
        except Exception as e:
            print(f"⚠️ [捕捉創傷] 運行中發生例外: {e}")
            SystemTraumaHandler.simulate_trauma("BRAIN_DEATH_CRASH")
            SystemHealingModule.heal_system("BRAIN_DEATH_CRASH")

        print("=" * 65)
        print(" ✨ [圓滿完成] Genesis-Core-Eternity 全生態系閉環運作完畢！")
        print("=" * 65)

if __name__ == "__main__":
    ecosystem = GenesisMasterEcosystem()
    # 執行合法且安全的完整生命週期管線
    ecosystem.run_full_lifecycle("EXECUTE_ACTION", "STANDARD_DATA_READ")

