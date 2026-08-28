import urllib.request
import json
import random
import time
from pathlib import Path

class AutonomousDaemonLab:
    def __init__(self, base_dir: str = "./", interval_seconds: int = 60):
        self.base_dir = Path(base_dir)
        self.precision_dir = self.base_dir / "species_precision"
        self.wild_dir = self.base_dir / "species_wild"
        self.interval = interval_seconds
        
        self.precision_dir.mkdir(exist_ok=True)
        self.wild_dir.mkdir(exist_ok=True)

    def fetch_raw_sources(self, query: str):
        print(f"\n[自動探針] 正在自動獵取目標: {query}")
        url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
        req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Autonomous-Bot', 'Accept': 'application/vnd.github.v3+json'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("items", [])[:2]
        except Exception as e:
            print(f"[X] 自動獵取失敗: {e}")
            return []

    def precision_track(self, item):
        print(f"[左側精準] 檢驗樣本: {item['name']}")
        is_valid = item.get("stargazers_count", 0) > 10 and item.get("description") is not None
        target_file = self.precision_dir / f"{item['name']}.json"
        
        if is_valid:
            clean_data = {
                "project": item["name"],
                "owner": item["owner"]["login"],
                "url": item["html_url"],
                "status": "survived"
            }
            target_file.write_text(json.dumps(clean_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f" [✓] 【生存】已歸入精準庫")
        else:
            if target_file.exists():
                target_file.unlink()
            print(f" [✕] 【銷毀】不合格，已清除")

    def wild_mutation_track(self, item_a, item_b):
        print(f"[右側野生] 混沌突變: {item_a['name']} x {item_b['name']}")
        chimera_name = f"{item_a['name']}_X_{item_b['name']}"
        target_file = self.wild_dir / f"{chimera_name}.txt"
        
        if random.random() < 0.8:
            target_file.write_text(f"Hybrid Success: {item_a['name']} & {item_b['name']}", encoding="utf-8")
            print(f" [✓] 【生存】誕生新物種: {chimera_name}")
        else:
            if target_file.exists():
                target_file.unlink()
            print(f" [✕] 【銷毀】突變失敗，殘骸已清除")

    def start_autonomous_loop(self):
        """啟動自主循環，讓它在背景自動運作"""
        print(f"=== 實驗室自主守護程序已啟動（間隔: {self.interval} 秒） ===")
        queries = ["LLM agent framework", "python automation tool", "ai scraping script"]
        
        try:
            while True:
                current_query = random.choice(queries)
                raw_items = self.fetch_raw_sources(current_query)
                
                if len(raw_items) >= 2:
                    self.precision_track(raw_items[0])
                    self.wild_mutation_track(raw_items[0], raw_items[1])
                else:
                    print("樣本不足，等待下次循環...")
                
                print(f"--- 循環結束，等待 {self.interval} 秒後再次出動 ---\n")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n[!] 守護程序收到手動中止指令，安全退場。")

if __name__ == "__main__":
    # 測試時設定每 10 秒自動抓取一次（正式運作可以調大秒數）
    lab = AutonomousDaemonLab(interval_seconds=10)
    lab.start_autonomous_loop()
