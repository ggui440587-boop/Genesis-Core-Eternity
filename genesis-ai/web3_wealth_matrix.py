import time
import requests
from bs4 import BeautifulSoup

class Web3WealthMatrix:
    def __init__(self, name="Termux-Web3-Matrix"):
        self.name = name
        # 涵蓋「投資、加密、區塊、賺錢」的全面性黃金關鍵字
        self.keywords = [
            "bitcoin", "btc", "ethereum", "eth", "solana", "crypto",
            "blockchain", "smart contract", "defi", "yield", "staking",
            "airdrop", "pump", "bull", "bear", "invest", "earn", "wealth",
            "listing", "launchpad", "alpha", "whale", "arbitrum", "optimism"
        ]
        print(f"[{self.name}] Web3 財富矩陣已啟動：鎖定 投資、加密、區塊、賺錢 全網情報...")

    def scout_web3_universe(self):
        # 全球公開的 Web3、區塊鏈與加密貨幣核心情報源
        targets = [
            {"url": "https://old.reddit.com/r/CryptoCurrency/hot/", "name": "Reddit CryptoCurrency (散戶風向與投資)"},
            {"url": "https://old.reddit.com/r/defi/hot/", "name": "Reddit DeFi (區塊鏈金融與收益)"},
            {"url": "https://old.reddit.com/r/ethdev/hot/", "name": "Reddit EthDev (智能合約與區塊鏈技術)"}
        ]
        
        intel_pool = []
        headers = {"User-Agent": "Mozilla/5.0 Web3WealthMatrixBot/5.0"}

        for target in targets:
            try:
                response = requests.get(target["url"], headers=headers, timeout=12)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    elements = soup.find_all(['a', 'h3', 'h2', 'p'])
                    
                    for el in elements:
                        text = el.get_text().strip()
                        lower_text = text.lower()
                        
                        # 只要包含上述任一黃金關鍵字，且長度足夠，即視為高價值情報
                        if len(text) > 18 and any(kw in lower_text for kw in self.keywords):
                            clean_title = text.replace('\n', ' ')
                            if clean_title not in [item['title'] for item in intel_pool]:
                                intel_pool.append({
                                    "source": target["name"],
                                    "title": clean_title[:150]
                                })
                time.sleep(2)
            except Exception as e:
                print(f"[{self.name}] 掃描 {target['name']} 時發生異常: {e}")
                
        return intel_pool

    def run(self):
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{timestamp}] 矩陣雷達正在掃描全網：投資、加密、區塊、賺錢...")
            
            signals = self.scout_web3_universe()
            
            if signals:
                filename = "web3_wealth_harvest.log"
                log_entry = f"\n==================== 矩陣財富報表: {timestamp} ===================+\n"
                log_entry += f"成功捕獲 {len(signals)} 筆區塊鏈投資與賺錢線索：\n"
                
                for idx, sig in enumerate(signals[:20], 1): # 取前 20 筆精華
                    log_entry += f"{idx}. [{sig['source']}] {sig['title']}\n"
                
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                
                print(f"[{self.name}] 成功！已將最新 Web3 財富情報寫入 {filename}")
            else:
                print(f"[{self.name}] 本輪暫無高匹配訊號，矩陣持續潛伏中...")
                
            # 每隔 30 分鐘自動執行一輪，緊釘市場脈動
            time.sleep(1800)

if __name__ == "__main__":
    matrix = Web3WealthMatrix()
    matrix.run()

