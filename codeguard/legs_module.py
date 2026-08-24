import os
import time

# ==============================================================
# System Legs Module - 系統雙腳與背景移動常駐模組 (象徵行動與跨目錄巡邏)
# ==============================================================

class SystemLegs:
    def __init__(self):
        self.current_position = os.getcwd()

    def walk_to_workspace(self, target_dir="."):
        """模擬雙腳移動：切換並確認當前的工作目錄路徑"""
        try:
            os.makedirs(target_dir, exist_ok=True)
            os.chdir(target_dir)
            self.current_position = os.getcwd()
            print(f"[雙腳移動] 成功跨步移動至工作路徑: {self.current_position}")
        except Exception as e:
            print(f"[雙腳錯誤] 移動失敗: {e}")

    def background_march(self):
        """模擬雙腳在背景持續行進與巡邏"""
        print("[雙腳常駐] 開始在背景穩健步行與巡邏...")
        for step in range(1, 4):
            print(f"-> [步行中] 第 {step } 步：當前所在位置保持穩固 ({self.current_position})")
            time.sleep(1)
        print("[雙腳完成] 巡邏步行告一段落，隨時準備前往下一個任務地點！")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🦵 系統雙腳與行動模組啟動")
    print("=" * 60)
    legs = SystemLegs()
    legs.walk_to_workspace()
    legs.background_march()

