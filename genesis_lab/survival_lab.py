import urllib.request
import json
import random
from pathlib import Path

class NaturalSelectionLab:
    def __init__(self, base_dir: str = "./"):
        self.base_dir = Path(base_dir)
        self.precision_dir = self.base_dir / "species_precision"
        self.wild_dir = self.base_dir / "species_wild"
        
        # 確保資料夾存在
        self.precision_dir.mkdir(exist_ok=True)
        self.wild_dir.mkdir(exist_ok=True)

    def fetch_raw_sources(self, query: str):
        """外部情報獵取"""
        print(f"[外部探針] 正在獵取目標: {query}")
        url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
        req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Survival-Bot', 'Accept': 'application/vnd.github.v3+json'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("items", [])[:2]
        except Exception as e:
            print(f"[X] 獵取失敗: {e}")
            return []

    def precision_track(self, item):
        """左側精準產線：驗證成功才存活，失敗直接銷毀"""
        print(f"\n[左側精準育種] 正在檢驗樣本: {item['name']}")
        
        # 模擬嚴格的基因與型態檢驗（例如檢查是否有敘述、有沒有被標星）
        is_valid = item.get("stargazers_count", 0) > 10 and item.get("description") is not None
        
        target_file = self.precision_dir / f"{item['name']}.json"
        
        if is_valid:
            clean_data = {
                "project": item["name"],
                "owner": item["owner"]["login"],
                "url": item["html_url"],
                "status": "survived_and_archived"
            }
            target_file.write_text(json.dumps(clean_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f" [✓] 檢驗合格！【生存】已歸入精準庫: {item['name']}")
        else:
            # 銷毀機制：確保不留殘骸
            if target_file.exists():
                target_file.unlink()
            print(f" [✕] 檢驗不合格！【銷毀】已徹底清除垃圾樣本: {item['name']}")

    def wild_mutation_track(self, item_a, item_b):
        """右側野生盲撞：強行混血，不穩定的直接淘汰"""
        print(f"\n[右側野生盲撞] 正在進行混沌突變: {item_a['name']} x {item_b['name']}")
        
        chimera_name = f"{item_a['name']}_X_{item_b['name']}"
        target_file = self.wild_dir / f"{chimera_name}.txt"
        
        # 模擬野生突變的隨機存活率（例如 80% 機率存活，20% 基因崩潰）
        mutation_survived = random.random() < 0.8
        
        if mutation_survived:
            payload = f"Mutated Hybrid Success. Combines {item_a['name']} & {item_b['name']}"
            target_file.write_text(payload, encoding="utf-8")
            print(f" [✓] 突變適應環境！【生存】誕生新物種: {chimera_name}")
        else:
            if target_file.exists():
                target_file.unlink()
            print(f" [✕] 基因嚴重排斥！【銷毀】突變失敗，已當場銷毀殘骸。")

if __name__ == "__main__":
    lab = NaturalSelectionLab()
    raw_items = lab.fetch_raw_sources("LLM agent framework")
    
    if len(raw_items) >= 2:
        # 左側精準育種審查
        lab.precision_track(raw_items[0])
        # 右側野生混血審查
        lab.wild_mutation_track(raw_items[0], raw_items[1])
    else:
        print("外部樣本不足，生態系暫停運作。")
