import time
import requests
import json

class WebScoutAgent:
    def __init__(self, name="Termux-Scout"):
        self.name = name
        print(f"[{self.name}] 網路探針初始化：準備出海探索公開網際網路...")

    def scout_github_trends(self):
        """
        利用公開的 GitHub API 抓取當前熱門專案（不需要任何 API Key）
        """
        print(f"[{self.name}] 正在連線至 GitHub 抓取公開熱門專案...")
        url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Termux-Agent-Client",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])[:5] # 取前 5 名
                
                report = "【聯網探針報告：GitHub 全球熱門專案】\n"
                for idx, repo in enumerate(items, 1):
                    name = repo.get("name")
                    stars = repo.get("stargazers_count")
                    desc = repo.get("description")
                    link = repo.get("html_url")
                    report += f"{idx}. 專案: {name} (⭐ {stars})\n   說明: {desc}\n   連結: {link}\n\n"
                
                return report
            else:
                return f"聯網成功，但伺服器回傳非預期狀態碼: {response.status_code}"
        except Exception as e:
            return f"聯網抓取失敗 (網路可能斷線或被阻擋): {e}"

    def act(self, report_content):
        """
        將聯網收集到的情報寫入本地日誌
        """
        filename = "network_scout.log"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}]\n{report_content}\n" + "="*50 + "\n"
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"[{self.name}] 探查完畢：情報已成功歸檔至 {filename}")

    def run_loop(self):
        print(f"[{self.name}] 啟動聯網探查任務...")
        
        # 執行網頁抓取
        intelligence = self.scout_github_trends()
        print("\n" + intelligence)
        
        # 寫入日誌
        self.act(intelligence)

if __name__ == "__main__":
    scout = WebScoutAgent()
    scout.run_loop()

