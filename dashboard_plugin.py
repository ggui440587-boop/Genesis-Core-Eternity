import time
import os
import glob

class ControlDashboardPlugin:
    def __init__(self, system_name="Termux-Matrix-Core"):
        self.system_name = system_name
        print(f"-> 🖥️ [面板外掛] 終端機控制儀表板初始化成功！")

    def render_dashboard(self):
        """渲染極度詳細的系統狀態面板"""
        # 收集即時數據
        plugin_files = glob.glob("*_plugin.py")
        total_plugins = len(plugin_files)
        
        total_lines = 0
        for fp in plugin_files:
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    total_lines += sum(1 for _ in f)
            except:
                pass

        os_load = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)

        print("\n" + "="*50)
        print(f" 🚀 {self.system_name} - 系統即時控制面板")
        print("="*50)
        print(sprintf_row("運行狀態", "🟢 正常運行 (ACTIVE)"))
        print(sprintf_row("當前時間", time.strftime("%Y-%m-%d %H:%M:%S")))
        print(sprintf_row("外掛總數", f"{total_plugins} 個模組"))
        print(sprintf_row("程式碼總行數", f"{total_lines} LOC"))
        print(sprintf_row("系統負載 (Load)", f"{os_load[0]}, {os_load[1]}, {os_load[2]}"))
        print("-"*50)
        print(" [詳細模組清單]:")
        for i, fp in enumerate(sorted(plugin_files), 1):
            print(f"   {i:2d}. 📦 {fp}")
        print("="*50 + "\n")

def sprintf_row(key, value):
    """協助排版對齊的輔助函式"""
    return f" 🔹 {key.ljust(15)} : {value}"

if __name__ == "__main__":
    dashboard = ControlDashboardPlugin()
    dashboard.render_dashboard()
