import os
import sys
import subprocess
import json
import datetime
import traceback

class ProductionUniversalCore:
    def __init__(self, workspace="."):
        self.workspace = workspace
        self.state_file = os.path.join(workspace, "system_evolution_state.json")
        self.log_file = os.path.join(workspace, "evolution_secure.log")
        self.load_state()

    def log(self, message):
        """真實寫入系統日誌檔案"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"寫入日誌失敗: {e}")

    def load_state(self):
        """讀取系統運行狀態（具備防呆與自動修復機制）"""
        self.state = {"runs": 0, "last_active": None}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.state.update(data)
            except Exception:
                pass

    def save_state(self):
        """儲存系統運行狀態"""
        self.state["runs"] = self.state.get("runs", 0) + 1
        self.state["last_active"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.log(f"儲存狀態失敗: {e}")

    def execute_shell_command(self, command):
        """真實執行系統 Shell 命令並回傳結果"""
        self.log(f"執行系統指令: {command}")
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, encoding="utf-8"
            )
            if result.returncode == 0:
                self.log("指令執行成功")
                return result.stdout.strip()
            else:
                self.log(f"指令執行錯誤: {result.stderr.strip()}")
                return result.stderr.strip()
        except Exception as e:
            self.log(f"執行指令發生例外: {e}")
            return str(e)

    def run_cycle(self):
        """執行核心主迴圈"""
        self.log("=== 啟動真實核心運作週期 ===")
        self.save_state()
        
        sys_info = self.execute_shell_command("uname -a")
        self.log(f"系統環境檢查完成: {sys_info}")
        self.log(f"目前累計執行次數: {self.state['runs']}")
        self.log("=== 核心運作週期結束 ===")

if __name__ == "__main__":
    core = ProductionUniversalCore()
    core.run_cycle()
