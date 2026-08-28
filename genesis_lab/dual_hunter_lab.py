import urllib.request
import json
import random
from pathlib import Path

def fetch_ai_sources(query: str):
    """向外部 GitHub 抓取兩份不同的 AI 專案清單"""
    print(f"[外部獵人] 正在發射探針搜尋: {query}")
    url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Bot', 'Accept': 'application/vnd.github.v3+json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            items = result.get("items", [])[:2] # 抓兩份
            return items
    except Exception as e:
        print(f"[X] 抓取失敗: {e}")
        return []

# ==================== 左側：正常育種與精準歸檔 ====================
def precision_track(item):
    print(f"\n[左側產線：精準育種]")
    print(f" > 接收安全樣本: {item['name']}")
    print(f" > 執行結構解析與型態檢查...")
    
    # 模擬精準處理與歸檔
    clean_data = {
        "project": item["name"],
        "author": item["owner"]["login"],
        "url": item["html_url"],
        "status": "normal_stable_archive"
    }
    
    Path("species_precision").mkdir(exist_ok=True)
    with open(f"species_precision/{item['name']}.json", "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
    print(f" [✓] 已精準收編並存入安全庫。")

# ==================== 右側：野生盲撞與基因混血 ====================
def wild_mutation_track(item_a, item_b):
    print(f"\n[右側產線：野生盲撞與混血]")
    print(f" > 隨機強制碰撞: [{item_a['name']}] x [{item_b['name']}]")
    
    # 模擬野蠻突變與混合
    chimera_name = f"{item_a['name']}_X_{item_b['name']}"
    mutation_result = f"Mutated AI Hybrid: Combines {item_a['description'] or 'None'} with {item_b['description'] or 'None'}"
    
    Path("species_wild").mkdir(exist_ok=True)
    with open(f"species_wild/{chimera_name}.txt", "w", encoding="utf-8") as f:
        f.write(mutation_result)
    print(f" [✓] 野生突變成功！誕生全新混血種: {chimera_name}")

if __name__ == "__main__":
    # 1. 抓取外部兩份情報
    raw_items = fetch_ai_sources("LLM agent python")
    
    if len(raw_items) >= 2:
        # 2. 分流處理：一份走正常精準育種，兩份一起丟進右側進行盲撞混血
        precision_track(raw_items[0])
        wild_mutation_track(raw_items[0], raw_items[1])
    else:
        print("外部樣本不足，暫緩雙軌作業。")
