import re
import time
import requests
from bs4 import BeautifulSoup

class DeepDiverAgent:
    def __init__(self, log_file="web3_code_wealth.log", output_file="intelligence_vault.md"):
        self.log_file = log_file
        self.output_file = output_file
        # 核心商業與技術價值過濾關鍵字
        self.focus_keywords = [
            "claude", "agent", "ai", "voice", "crypto", "bitcoin", 
            "ethereum", "blockchain", "defi", "yield", "automation", 
            "bot", "script", "tool", "github.com/"
        ]
        print("[Deep-Diver] 深度挖掘與智慧過濾引擎已啟動...")

    def smart_filter_and_dive(self):
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"[Deep-Diver] 找不到日誌檔 {self.log_file}，請確保主雷達正在運作。")
            return

        # 抓取所有包含通道連結的項目
        entries = re.findall(r'\[(.*?)\] (.*?) \(通道: (.*?)\)', content)
        
        filtered_vault = []
        seen_links = set()

        print(f"[Deep-Diver] 正在從日誌中過濾高價值標的...")

        for source, title, link in entries:
            # 確保不重複且包含關注的關鍵字
            combined_text = f"{title} {link}".lower()
            if link in seen_links:
                continue
            
            if any(kw in combined_text for kw in self.focus_keywords):
                seen_links.add(link)
                item_info = {
                    "source": source,
                    "title": title.strip(),
                    "link": link.strip(),
                    "summary": "尚未深入挖掘",
                    "install": "尚未深入挖掘"
                }
                
                # 如果是 GitHub 專案，派分身進行「深度挖掘 (Deep Dive)」
                if "github.com/" in link and not link.endswith("sponsors") and not link.endswith("security"):
                    print(f"[Deep-Diver] 正在深入挖掘 GitHub 專案: {link}")
                    readme_info = self.fetch_github_readme(link)
                    if readme_info:
                        item_info["summary"] = readme_info.get("summary", "精準摘要擷取中...")
                        item_info["install"] = readme_info.get("install", "請見專案首頁")
                    time.sleep(1.5) # 禮貌性延遲，避免請求過快

                filtered_vault.append(item_info)

        # 寫入專屬的技術情報庫 (Markdown 格式)
        self.save_to_vault(filtered_vault)

    def fetch_github_readme(self, repo_url):
        headers = {"User-Agent": "Mozilla/5.0 DeepDiverAgent/1.0"}
        try:
            res = requests.get(repo_url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # 試圖抓取 GitHub 專案的描述 (about / description)
                desc_meta = soup.find("meta", property="og:description")
                summary = desc_meta["content"] if desc_meta else "無詳細描述"
                
                # 嘗試尋找安裝或快速開始的提示
                install_text = "標準 Python/Git 專案，可透過 git clone 下載後查看 README。"
                body_text = soup.get_text().lower()
                if "pip install" in body_text:
                    install_text = "支援 pip install 安裝"
                elif "npm install" in body_text:
                    install_text = "支援 npm install 安裝"
                
                return {
                    "summary": summary[:200],
                    "install": install_text
                }
        except Exception as e:
            print(f"[Deep-Diver] 挖掘 {repo_url} 時發生例外: {e}")
        return None

    def save_to_vault(self, vault_data):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        md_content = f"# 🧠 專屬技術與財富情報庫\n\n> 最後更新時間: {timestamp}\n\n"
        md_content += f"總計篩選並深度挖掘出 **{len(vault_data)}** 個高價值核心項目：\n\n---\n\n"

        for idx, item in enumerate(vault_data, 1):
            md_content += f"### {idx}. {item['title']}\n"
            md_content += f"- **情報來源**: `{item['source']}`\n"
            md_content += f"- **直達通道**: [{item['link']}]({item['link']})\n"
            md_content += f"- **核心摘要**: {item['summary']}\n"
            md_content += f"- **安裝/運作提示**: `{item['install']}`\n\n"

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"[Deep-Diver] 成功！情報庫已更新至 {self.output_file}")

if __name__ == "__main__":
    diver = DeepDiverAgent()
    diver.smart_filter_and_dive()

