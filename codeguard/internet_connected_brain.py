import urllib.request
import json

class InternetConnectedBrain:
    def __init__(self):
        print("-> 🌐 [外部網路大腦] 初始化完成：準備透過網際網路連接真實世界資料。")

    def fetch_real_world_data(self):
        """透過真實外部網路取得公開的網路資料（以公開的 IP 查詢 API 為例）"""
        target_api = "https://httpbin.org/ip"
        print(f"\n-> 🌍 [網路連線中] 正在透過網際網路請求真實外部服務: {target_api}")

        try:
            # 發送真實的網際網路請求
            with urllib.request.urlopen(target_api, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                print(f"-> [✔] 成功連線至真實世界！取得外部回應資料: {data}")
                return data
        except Exception as e:
            print(f"-> [❌] 外部網路連線失敗: {e}")
            return None

    def process_and_command_robot(self):
        """大腦分析外部網路資料，並產生對應的機器人指令"""
        external_data = self.fetch_real_world_data()

        if external_data:
            print(f"-> 🧠 [大腦分析] 成功解析外部網路狀態，開始轉換機器人指令...")
            action = "SYNC_WITH_EXTERNAL_CLOUD"
        else:
            print(f"-> 🧠 [大腦分析] 無法取得外部網路資料，切換為本地離線安全模式...")
            action = "OFFLINE_SAFE_MODE"

        print(f"-> 🤖 [機器人指令生成] 決定執行的虛擬動作: {action}")

if __name__ == "__main__":
    brain = InternetConnectedBrain()
    brain.process_and_command_robot()

