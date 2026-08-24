import os
import sqlite3
import base64
import requests

class MatrixMonetizeVault:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[Vault-Monetize-Core] 正在初始化純 Python 內建加密保險箱與自動變現漏斗...")
        self.init_vault_security()

    def init_vault_security(self):
        """初始化內建安全資料表"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secure_vault_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_title TEXT,
                encrypted_payload TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("[🛡️ 保險箱] 內建安全資料表已就緒。")

    def simple_encrypt(self, text, shift=3):
        """輕量混淆加密（純 Python 內建，無需編譯）"""
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        # 進行簡單的字元位移混淆
        return "".join([chr(ord(c) + shift) for c in encoded_bytes.decode('utf-8')])

    def simple_decrypt(self, encrypted_text, shift=3):
        """輕量混淆解密"""
        try:
            decoded_shifted = "".join([chr(ord(c) - shift) for c in encrypted_text])
            return base64.b64decode(decoded_shifted.encode('utf-8')).decode('utf-8')
        except Exception:
            return "[❌ 解密失敗]"

    def secure_database_export(self):
        """將智庫機密資料進行加密備份"""
        print("[🛡️ 保險箱] 正在執行智庫加密備份與防護掃描...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT title FROM intel_vault ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            title = row[0]
            encrypted = self.simple_encrypt(title)
            cursor.execute("INSERT INTO secure_vault_log (item_title, encrypted_payload) VALUES (?, ?)", (title, encrypted))
            conn.commit()
            print(f"[✅ 保險箱] 成功將最新情報加密封存至安全保險箱內。")
        conn.close()

    def run_monetization_funnel(self):
        """自動化變現與內容分發漏斗"""
        print("[💰 變現漏斗] 正在將智庫情報煉金為高流量變現文案...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT title, link FROM intel_vault ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("[⚠️ 變現漏斗] 智庫尚無可分發的內容。")
            return

        title, link = row
        monetize_post = (
            f"🔥 【矩陣特工獨家情報】\n\n"
            f"{title}\n\n"
            f"👉 深度洞察與原始通道：{link}\n\n"
            f"#開源自動化 #資訊差 #Web3 #數位帝國"
        )

        print(f"\n--- 🚀 生成的自動變現/流量貼文預覽 ---\n{monetize_post}\n------------------------------------------")
        
        token = os.environ.get("TG_BOT_TOKEN", "YOUR_BOT_TOKEN")
        chat_id = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID")
        if token != "YOUR_BOT_TOKEN" and chat_id != "YOUR_CHAT_ID":
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            try:
                res = requests.post(url, json={"chat_id": chat_id, "text": monetize_post, "parse_mode": "Markdown"}, timeout=10)
                if res.status_code == 200:
                    print("[✅ 流量漏斗] 變現文案已成功自動發布至公開頻道！")
            except Exception as e:
                print(f"[❌ 發布失敗] {e}")
        else:
            print("[ℹ️ 提示] Telegram 頻道尚未設定完整，已完成本地煉金與變現排程模擬。")

    def execute_empire_cycle(self):
        self.secure_database_export()
        self.run_monetization_funnel()

if __name__ == "__main__":
    core = MatrixMonetizeVault()
    core.execute_empire_cycle()

