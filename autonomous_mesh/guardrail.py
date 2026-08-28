class SecurityGuardrail:
    def __init__(self):
        self.ALLOWED_ACTIONS = ["analyze_logs", "scan_network", "optimize_memory"]

    def inspect(self, intent: dict) -> tuple[bool, str]:
        action = intent.get("action")
        if action not in self.ALLOWED_ACTIONS:
            return False, f"動作 '{action}' 違反白名單規範。"
        
        intent_str = str(intent).lower()
        if any(keyword in intent_str for keyword in ["delete", "sudo", "rm ", "sh"]):
            return False, "偵測到具備破壞性或越權的高風險指令。"
            
        return True, "安全檢查通過"

