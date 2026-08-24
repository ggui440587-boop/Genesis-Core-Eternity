import time
import requests
from bs4 import BeautifulSoup

class Web3CodeMatrix:
    def __init__(self, name="Termux-Web3-Code-Hunter"):
        self.name = name
        # 同時鎖定：開源程式、區塊鏈、加密貨幣、賺錢投資
        self.keywords = [
            "python", "script", "bot", "github", "opensource", "tool",
            "crypto", "bitcoin", "ethereum", "blockchain", "smart contract",
            "defi", "yield", "airdrop", "pump", "invest", "earn"
        ]
        print(f"[{self.name}] 開源與財富矩陣啟動：全面掃描 程式、區塊鏈、加密、賺錢...")

    def scout_sources(self):
        # 鎖定 GitHub 趨勢與幣圈公開集散地
        targets = [
            {"url": "https://github.com/trending/python", "name": "GitHub Python Trending (最新開源程式)"},
            {"url": "https://old.reddit.com/r/CryptoCurrency/hot/", "name": "Reddit Crypto (加密投資風向)"},
            {"url": "https://old.reddit.com/r/defi/hot/", "name": "Reddit DeFi (區塊鏈與賺錢協議)"}
        ]
        
        harvests = []
        headers = {"User-Agent": "Mozilla/5.0 Web3CodeMatrixBot/6.0"}

        for target in targets:
            try:
                response = requests.get(target["url"], headers=headers, timeout=12)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    elements = soup.find_all(['a', 'h3', 'h2', 'p'])
                    
                    for el in elements:
                        text = el.get_text().strip()
                        lower_text = text.lower()
                        
                        # 只要包含關鍵字，就擷取下來
                        if len(text) > 15 and any(kw in lower_text for kw in self.keywords):
                            clean_title = text.replace('\n', ' ')
                            link = el.get('href', '#')
                            if not link.startswith('http'):
                                link = "GitHub/Community"
                                
                            item_entry = f"[{target['name']}] {clean_title[:120]} (通道: {link})"
                            if item_entry not in [h['entry'] for h in harvests]:
                                harvests.append({"entry": item_entry})
                time.sleep(2)
            except Exception as e:
                print(f"[{self.name}] 掃描 {target['name']} 異常: {e}")
                
        return harvests

    def run(self):
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{timestamp}] 正在全網搜羅：開源程式、區塊鏈、加密、賺錢情報...")
            
            data = self.scout_sources()
            
            if data:
                filename = "web3_code_wealth.log"
                log_content = f"\n==================== 戰利品報表: {timestamp} ====================\n"
                log_content += f"共捕獲 {len(data)} 筆開源程式與區塊鏈投資線索：\n"
                
                for i, item in enumerate(data[:20], 1):
                    log_content += f"{i}. {item['entry']}\n"
                
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_content)
                
                print(f"[{self.name}] 成功！已將開源與鏈上情報寫入 {filename}")
            else:
                print(f"[{self.name}] 本輪暫無高匹配標的，繼續潛伏...")
                
            # 每隔 30 分鐘自動執行一輪
            time.sleep(1800)

if __name__ == "__main__":
    matrix = Web3CodeMatrix()
    matrix.run()

