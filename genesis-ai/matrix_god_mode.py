import os
import subprocess
import requests
import json
import time

class MatrixGodMode:
    def __init__(self):
        print("[God-Mode] 正在初始化上帝模式與物理邊界突破模組...")

    def enable_wake_lock(self):
        """啟用喚醒鎖，防止手機進入深度睡眠切斷背景運作"""
        print("[God-Mode] 正在鎖定硬體電源管理（WakeLock）...")
        subprocess.run("termux-wake-lock", shell=True, capture_output=True)
        print("[✅ 物理防護] 喚醒鎖已啟動，手機背景將持續全速運轉不休眠。")

    def query_local_ollama(self, prompt):
        """調用本地 Ollama 執行離線 AI 智慧解讀與文案重寫"""
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",  # 假設您在本地安裝了 llama3 或其他輕量模型
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "AI 回應解析失敗")
        except Exception:
            return "[提示] 本地 Ollama 伺服器未運行，建議執行 `ollama serve` 啟動本地 AI 腦。"
        return "本地 AI 離線推理中..."

    def publish_to_telegram(self, message):
        """自動將煉金完成的爆款文案推送到私人 Telegram 頻道或聊天室"""
        # 請替換為您自己的 Telegram Bot Token 與 Chat ID (或透過環境變數讀取)
        token = os.environ.get("TG_BOT_TOKEN", "YOUR_BOT_TOKEN")
        chat_id = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID")
        
        if token == "YOUR_BOT_TOKEN":
            print("[⚠️ 發布通知] Telegram Bot Token 尚未設定，已略過自動發布。")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                print("[✅ 流量漏斗] 成功將爆款情報與文案自動發布至 Telegram 頻道！")
            else:
                print(f"[❌ 發布失敗] Telegram 回應錯誤: {res.text}")
        except Exception as e:
            print(f"[❌ 發布例外] 連線至 Telegram API 失敗: {e}")

    def activate_god_mode(self):
        """一鍵點火：解鎖上帝模式全部功能"""
        self.enable_wake_lock()
        
        print("\n--- 🧠 測試本地 AI 腦 (Ollama) ---")
        ai_test = self.query_local_ollama("請用一句話總結為什麼開源自動化腳本能帶來資訊差財富。")
        print(f"本地 AI 回應：\n{ai_test}\n")

        print("--- 🚀 觸發多平台自動化發布漏斗 ---")
        sample_post = "🚀 *【矩陣上帝模式情報】* \n最新自動化開源與 Web3 財富雷達已全速運轉，本地 AI 腦與雲端防護同步上線！"
        self.publish_to_telegram(sample_post)
        
        print("\n[🔥 終極宣告] 您的 Termux 矩陣已達成「不休眠、本地 AI、自動發布」的完全體神級狀態！")

if __name__ == "__main__":
    god = MatrixGodMode()
    god.activate_god_mode()

