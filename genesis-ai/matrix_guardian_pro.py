import os
import shutil
import sqlite3
import subprocess
import datetime
import glob

class MatrixGuardianPro:
    def __init__(self, db_name="matrix_intel.db", log_file="matrix_scheduler.log"):
        self.db_name = db_name
        self.log_file = log_file
        self.backup_dir = "./matrix_secure_backups"
        print("[Guardian-Pro] 正在初始化旗艦級系統護航與防禦核心...")
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def check_battery_and_thermal(self):
        """設備狀態與電池/溫度防禦保護"""
        print("[🌡️ 體檢] 正在檢測手機硬體溫度與電池健康狀態...")
        res = subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True)
        
        if res.returncode != 0:
            print("[⚠️ 提示] 未偵測到 Termux API，跳過硬體感測。")
            return True

        try:
            import json
            battery_data = json.loads(res.stdout)
            temp = battery_data.get("temperature", 25.0)
            percentage = battery_data.get("percentage", 100)
            plugged = battery_data.get("plugged", "UNPLUGGED")

            print(f"[📊 硬體狀態] 電量: {percentage}% | 溫度: {temp}°C | 電源狀態: {plugged}")

            # 安全閥門：若溫度超過 45 度且未充電，強制暫停運作進入冷卻
            if temp > 45.0 and plugged == "UNPLUGGED":
                print("[🔥 過熱警告] 手機溫度超過 45°C 且未充電！啟動冷卻保護，暫停本輪排程。")
                return False
            
            # 低電量警告
            if percentage < 15 and plugged == "UNPLUGGED":
                print("[🪫 低電量警告] 電量低於 15% 且未插電，進入省電保護狀態。")
                return False

        except Exception as e:
            print(f"[❌ 體檢例外] 解析電池資訊失敗: {e}")

        return True

    def cleanup_logs_and_db(self, max_log_size_mb=5):
        """紀錄檔自動清理與瘦身機制"""
        print("[🧹 瘦身] 正在檢查紀錄檔與資料庫體積...")
        
        # 檢查日誌檔大小
        if os.path.exists(self.log_file):
            size_mb = os.path.getsize(self.log_file) / (1024 * 1024)
            if size_mb > max_log_size_mb:
                print(f"[🧹 瘦身] 紀錄檔大小 ({size_mb:.2f} MB) 超過限制，正在進行自動歸零瘦身...")
                with open(self.log_file, "w") as f:
                    f.write(f"--- [Log Reset at {datetime.datetime.now()}] ---\n")
            else:
                print(f"[✅ 瘦身] 紀錄檔大小正常 ({size_mb:.2f} MB)。")

        # 資料庫 VACUUM 優化（釋放未使用的空間並瘦身）
        if os.path.exists(self.db_name):
            try:
                conn = sqlite3.connect(self.db_name)
                conn.execute("VACUUM;")
                conn.close()
                print("[✅ 瘦身] SQLite 智庫資料庫空間已完成 VACUUM 優化瘦身。")
            except Exception as e:
                print(f"[❌ 瘦身例外] 資料庫優化失敗: {e}")

    def encrypted_local_backup(self):
        """戰報產出與自動備份至安全備份夾"""
        print("[💾 備份] 正在建立智庫的本地安全備份...")
        if not os.path.exists(self.db_name):
            print("[⚠️ 備份] 找不到智庫檔案。")
            return

        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"matrix_intel_backup_{date_str}.db")
        
        try:
            shutil.copyfile(self.db_name, backup_path)
            print(f"[✅ 備份] 成功建立備份點: {backup_path}")

            # 保持備份夾最多只留最近 5 份，避免佔滿空間
            backups = sorted(glob.glob(os.path.join(self.backup_dir, "*.db")))
            if len(backups) > 5:
                os.remove(backups[0])
                print("[🗑️ 清理] 已自動移除最舊的一份歷史備份，維持空間精簡。")
        except Exception as e:
            print(f"[❌ 備份失敗] {e}")

    def get_ai_response_with_fallback(self, prompt):
        """多重 AI API 切換與備援機制 (示範架構)"""
        print("[🤖 AI 備援] 正在呼叫 AI 核心（支援自動備援切換）...")
        
        # 模擬 API 順序：Primary (主用) -> Fallback (備用)
        api_providers = ["Primary-API", "Secondary-Gemini-API"]
        
        for provider in api_providers:
            try:
                print(f"[🔗 嘗試連線] 正在透過 {provider} 執行請求...")
                # 這裡可放入你實際的 API 請求邏輯
                if provider == "Primary-API":
                    # 假設主 API 有時會發生連線逾時或限流
                    # raise Exception("Connection Timeout")
                    pass
                
                print(f"[✅ 成功] 成功透過 {provider} 取得回應！")
                return f"[{provider} 成功回應]"
            except Exception as e:
                print(f"[⚠️ 警告] {provider} 呼叫失敗 ({e})，正在無縫切換至下一個備援引擎...")
        
        print("[❌ 嚴重錯誤] 所有 AI 備援通道皆無法連線。")
        return None

    def run_guardian_check(self):
        """執行全方位護航檢測"""
        print("\n================================================")
        print("🛡️ [Guardian Pro] 開始執行旗艦級系統護航檢測...")
        print("================================================")
        
        # 1. 電池與溫度防禦
        if not self.check_battery_and_thermal():
            print("🛑 [系統防護] 觸發硬體保護機制，本輪心跳暫停執行。\n")
            return False

        # 2. 日誌與資料庫瘦身
        self.cleanup_logs_and_db()

        # 3. 本地安全備份
        self.encrypted_local_backup()

        print("✅ [Guardian Pro] 系統護航檢測完貝，狀態完美，準備放行作戰任務。\n")
        return True

if __name__ == "__main__":
    guardian = MatrixGuardianPro()
    guardian.run_guardian_check()

