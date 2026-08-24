# ==============================================================
# System Immunization Core - 全系統免疫與安全主控防線
# ==============================================================

from security_firewall import SecurityFirewall
from system_trauma_module import SystemTraumaHandler
from system_healing_module import SystemHealingModule

class SystemImmunizationCore:
    @staticmethod
    def safe_execute_pipeline(command_tag, trauma_trigger=None):
        """安全執行的免疫防護管線：檢查 -> 執行 -> 捕捉創傷 -> 自動修復"""
        print("=" * 60)
        print(f" 🛡️ [免疫主控] 啟動全系統安全防護管線，指令目標: [{command_tag}]")
        print("=" * 60)

        # 1. 步驟一：透過安全防護牆檢查權限
        is_allowed = SecurityFirewall.inspect_request(command_tag)

        if not is_allowed:
            print("-> [防線攔截] 請求遭拒，管線中止。")
            return

        # 2. 步驟二：模擬執行與創傷捕捉
        try:
            if trauma_trigger:
                SystemTraumaHandler.simulate_trauma(trauma_trigger)
            else:
                print(f"-> [執行正常] 指令 [{command_tag}] 運行順利，無異常創傷。")
        except Exception:
            # 3. 步驟三：若發生異常，交由修復模組進行自動再生
            print("-> [觸發防禦] 捕捉到執行例外，轉交醫療中心...")
            SystemHealingModule.heal_system(trauma_trigger)

if __name__ == "__main__":
    # 測試 1：合法且無創傷的正常執行
    SystemImmunizationCore.safe_execute_pipeline("EXECUTE_ACTION")

    print("\n" + "=" * 60 + "\n")

    # 測試 2：合法但帶有記憶體外洩創傷的執行與自動修復
    SystemImmunizationCore.safe_execute_pipeline("SYSTEM_HEAL", "BLEEDING_MEMORY_LEAK")

