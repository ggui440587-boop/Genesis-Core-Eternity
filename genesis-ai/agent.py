import time
import requests

class NetworkAgent:
    def __init__(self, name="Termux-Net-Bot"):
        self.name = name
        print(f"[{self.name}] 初始化完成：準備連線至公用網路（不需任何 API）")

    def fetch_public_data(self):
        """
        利用網路抓取公開的免費資料（以 GitHub 的公共 API 或公開網頁為例）
        """
        print(f"[{self.name}] 正在透過網路抓取公用數據...")
        try:
            # 抓取 GitHub 公開的熱門 Python 專案資訊（不需要 API Key 也能訪問）
            url = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc"
            
            # 加上 User-Agent 模擬瀏覽器
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 簡單提取前幾個熱門專案的名字
                top_repo = data['items'][0]['name']
                repo_url = data['items'][0]['html_url']
                return f"成功連線網路！當前 GitHub 最熱門的 Python 專案是：{top_repo} ({repo_url})"
            else:
                return f"網路請求成功，但伺服器回傳狀態碼：{response.status_code}"
                
        except Exception as e:
            return f"網路連線異常: {e}"

    def act(self, content):
        filename = "net_activity.log"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{content}\n" + "-"*40 + "\n")
        print(f"[{self.name}] 聯網結果已寫入日誌。")

    def run(self):
        result = self.fetch_public_data()
        print(result)
        self.act(result)

if __name__ == "__main__":
    bot = NetworkAgent()
    bot.run()

