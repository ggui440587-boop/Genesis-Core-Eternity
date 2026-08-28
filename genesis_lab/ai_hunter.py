import urllib.request
import json
from pathlib import Path

def process(query: str = "ai python script"):
    """
    對外爬蟲介面：以關鍵字去外部搜尋 AI 相關專案或資料，並抓回本地
    """
    print(f"[AI 獵人] 正在向外部搜尋與 '{query}' 相關的專案情報...")
    
    url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
    
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Genesis-Core-Eternity-Bot',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            items = result.get("items", [])[:3]
            
            harvested_info = []
            for item in items:
                repo_info = {
                    "name": item["name"],
                    "owner": item["owner"]["login"],
                    "description": item["description"],
                    "clone_url": item["clone_url"],
                    "stars": item["stargazers_count"]
                }
                harvested_info.append(repo_info)
                print(f"[✓] 捕獲目標: {repo_info['name']} (Stars: {repo_info['stars']})")
                
            return harvested_info
            
    except Exception as e:
        print(f"[X] 外部獵取失敗: {str(e)}")
        return []

if __name__ == "__main__":
    data = process("AI agent")
    print(json.dumps(data, indent=2, ensure_ascii=False))
