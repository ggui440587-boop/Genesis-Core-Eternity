import urllib.request
import json
import random
import time
from pathlib import Path

class AutonomousExplorerLab:
    def __init__(self, base_dir: str = "./"):
        self.base_dir = Path(base_dir)
        self.precision_dir = self.base_dir / "species_precision"
        self.wild_dir = self.base_dir / "species_wild"
        
        self.precision_dir.mkdir(exist_ok=True)
        self.wild_dir.mkdir(exist_ok=True)
        
        # 初始的探索種子方向，它會根據抓回來的結果自己長出新方向
        self.active_directions = ["AI agent", "python automation", "web scraper", "vector database"]

    def generate_new_direction(self, recent_item):
        """核心：根據抓回來的真實專案特徵，自主衍生出下一個探索方向"""
        desc = recent_item.get("description") or ""
        name = recent_item.get("name") or ""
        
        # 從專案名稱或描述中提取關鍵字來當作新方向的靈感
        words = [w.lower() for w in (name + " " + desc).split() if len(w) > 4]
        if words:
            new_seed = random.choice(words)
            dynamic_direction = f"python {new_seed}"
            if dynamic_direction not in self.active_directions:
                self.active_directions.append(dynamic_direction)
                print(f"[雷達擴張] 偵測到新領域！自主衍生出探索方向: [{dynamic_direction}]")

    def fetch_raw_sources(self):
        """自主決定方向去外面抓資料"""
        current_query = random.choice(self.active_directions)
        print(f"\n[自主探針] 雷達鎖定方向 -> 關鍵字: {current_query}")
        
        url = f"https://api.github.com/search/repositories?q={urllib.request.quote(current_query)}+language:python&sort=stars&order=desc"
        req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Explorer-Bot', 'Accept': 'application/vnd.github.v3+json'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                items = result.get("items", [])[:2]
                if items:
                    # 啟動動態衍生機制
                    self.generate_new_direction(items[0])
                return items
        except Exception as e:
            print(f"[X] 探索失敗: {e}")
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
            print(f" [✓] 【生存】已收編進精準庫")
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

    def start_exploration_loop(self, interval: int = 10):
        print(f"=== 自主探索實驗室已啟動（動態雷達運行中） ===")
        try:
            while True:
                raw_items = self.fetch_raw_sources()
                if len(raw_items) >= 2:
                    self.precision_track(raw_items[0])
                    self.wild_mutation_track(raw_items[0], raw_items[1])
                else:
                    print("此方向樣本不足，切換下一個雷達目標...")
                
                print(f"--- 探索循環暫停 {interval} 秒 ---\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[!] 探索程序已安全中止。")

if __name__ == "__main__":
    lab = AutonomousExplorerLab()
    lab.start_exploration_loop(interval_10 := 10)
