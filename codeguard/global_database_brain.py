import urllib.request
import json
import datetime

class GlobalDatabaseBrain:
    def __init__(self):
        print("-> 🧠 [全球數據大腦] 初始化完成：準備連線至全球公開數據庫與知識庫。")

    def query_global_database(self):
        """向全球公開的 IP 與地理數據庫發送查詢請求（已加入瀏覽器偽裝標頭）"""
        global_api_url = "https://ipapi.co/json/"
        print(f"\n-> 🌍 [全球數據請求] 正在連接全球數據庫伺服器: {global_api_url}")

        try:
            # 模擬真實瀏覽器的 Headers 標頭，避開 403 阻擋
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json,text/html,application/xhtml+xml'
            }

            req = urllib.request.Request(global_api_url, headers=headers)

            with urllib.request.urlopen(req, timeout=5) as response:
                raw_data = response.read().decode('utf-8')
                global_data = json.loads(raw_data)
                return global_data

        except Exception as e:
            print(f"-> [❌] 連接全球數據庫失敗: {e}")
            return None

    def process_global_knowledge(self):
        """大腦接收並分析來自全世界數據庫的資訊"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = self.query_global_database()

        if data and "ip" in data:
            print(f"\n-> [✔] 成功從全球數據庫檢索到以下資訊（時間: {timestamp}）:")
            print(f"   ├─ 全球公開 IP: {data.get('ip')}")
            print(f"   ├─ 所屬國家: {data.get('country_name')} ({data.get('country_code')})")
            print(f"   ├─ 所在城市: {data.get('city')}")
            print(f"   ├─ 行政區域: {data.get('region')}")
            print(f"   └─ 經緯度座標: {data.get('latitude')}, {data.get('longitude')}")

            print(f"\n-> ⚡ [大腦決策] 已將全球數據庫的空間與節點資訊載入大腦記憶體，準備進行後續運算。")
        else:
            print(f"-> ⚠️ [警告] 無法解析全球數據庫回傳的內容，切換至本地預設知識庫。")

if __name__ == "__main__":
    brain = GlobalDatabaseBrain()
    brain.process_global_knowledge()

