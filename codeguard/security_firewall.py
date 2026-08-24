# ==============================================================
# Security Firewall & Access Control Module - 系統安全防護牆與存取控制
# ==============================================================

class SecurityFirewall:
    # 定義允許存取系統的核心權限白名單指令
    AUTHORIZED_COMMANDS = [
        "READ_KNOWLEDGE",
        "EXECUTE_ACTION",
        "SYSTEM_HEAL",
        "HEARTBEAT_PULSE"
    ]

    @classmethod
    def inspect_request(cls, command_tag):
        """檢查並過濾進入系統的指令請求是否合法"""
        print("=" * 50)
        print(f" 🛡️ [安全防護牆] 正在檢測外部或模組請求權限: [{command_tag}]")
        print("=" * 50)

        if command_tag in cls.AUTHORIZED_COMMANDS:
            print(f"-> [存取允許] 🟢 指令 [{command_tag}] 通過安全檢驗，執行中...")
            return True
        else:
            print(f"-> [存取攔截] 🔴 警告！偵測到未授權的非法指令: [{command_tag}]，已安全阻斷。")
            return False

if __name__ == "__main__":
    # 測試合法指令
    SecurityFirewall.inspect_request("EXECUTE_ACTION")
    print("-" * 50)
    # 測試非法入侵指令
    SecurityFirewall.inspect_request("MALICIOUS_INJECTION_ATTACK")
