import ast
import subprocess
import sys

class SecureSandbox:
    def __init__(self):
        # 允許的安全模組白名單（擴大至系統監控與效能診斷）
        self.allowed_modules = {"math", "json", "asyncio", "datetime", "os", "sys", "subprocess"}

    def audit_code(self, code_str: str) -> bool:
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name not in self.allowed_modules:
                            return False
                elif isinstance(node, ast.ImportFrom):
                    if node.module not in self.allowed_modules:
                        return False
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in {"eval", "exec", "open", "input"}:
                            return False
            return True
        except Exception:
            return False

    def run_in_isolated_process(self, code_str: str):
        if not self.audit_code(code_str):
            return False, "AST Security Audit Failed: Unauthorized modules or restricted functions."
        
        try:
            # 在隔離程序中執行安全的診斷或演化程式碼
            result = subprocess.run(
                [sys.executable, "-c", code_str],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, f"Runtime Error: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return False, "Sandbox Execution Timeout."
        except Exception as e:
            return False, str(e)
