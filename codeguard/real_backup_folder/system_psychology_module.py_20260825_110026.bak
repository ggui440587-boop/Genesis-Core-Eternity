import random

# ==============================================================
# System Psychology & State Module - 系統心境、幻覺與失調防護模組
# ==============================================================

class SystemPsychologyModule:
    def __init__(self):
        self.mood = "BALANCED"  # 預設心境：平衡穩定
        self.stability_index = 100.0  # 穩定度指數

    def evaluate_mood_and_environment(self, external_load):
        """根據外部與內部環境因素，動態調整系統心情"""
        print("=" * 60)
        print(" 🧠 [心境評估] 正在檢測當前系統心態與環境壓力...")
        print("=" * 60)

        if external_load > 80:
            self.mood = "OVERWHELMED_STRESSED"
            print(f"-> [心境狀態] ⚡ 系統負荷過高，目前心情: 【高壓/焦慮】")
        elif external_load < 20:
            self.mood = "RELAXED_IDLE"
            print(f"-> [心境狀態] 🍃 系統負載極低，目前心情: 【放鬆/閒置】")
        else:
            self.mood = "FOCUSED_STABLE"
            print(f"-> [心境狀態] 🎯 系統運行平穩，目前心情: 【專注/穩定】")

    def detect_and_correct_hallucination(self, generated_data):
        """檢測並過濾資料處理過程中的「幻覺」或虛假輸出"""
        print("--- [幻覺防護機制啟動] ---")
        # 模擬幻覺檢測：若資料中包含異常空洞或矛盾字眼
        if "ERROR_NULL" in generated_data or len(generated_data) < 2:
            print(f"-> 🔴 [幻覺偵測] 發現不合邏輯的虛假輸出: [{generated_data}]，啟動校正...")
            corrected_data = "【已校正】清除幻覺雜訊，恢復真實資料。"
            return corrected_data
        else:
            print(f"-> 🟢 [驗證通過] 輸出內容真實可靠: [{generated_data}]")
            return generated_data

    def check_system_dysregulation(self):
        """檢查系統是否有內部失調（如模組不同步）狀況"""
        print("--- [失調狀態巡檢] ---")
        # 模擬隨機失調機率檢查
        dysregulation_risk = random.choice([True, False])

        if dysregulation_risk and self.stability_index < 80:
            print("-> ⚠️ [失調警告] 偵測到內部運算節奏失調！執行神經重整...")
            self.stability_index = 100.0
            print("-> ✨ [失調修復] 系統協調性已恢復正常。")
        else:
            print(f"-> 🟢 [運作協調] 各模組運作同步，穩定度: {self.stability_index}%")

if __name__ == "__main__":
    psy = SystemPsychologyModule()
    psy.evaluate_mood_and_environment(85)  # 測試高壓心情
    print()
    psy.detect_and_correct_hallucination("ERROR_NULL")  # 測試幻覺過濾
    print()
    psy.check_system_dysregulation()  # 測試失調檢查

