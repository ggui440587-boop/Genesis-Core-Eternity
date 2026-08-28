import re
import glob

class ObsidianGraphPlugin:
    def __init__(self, vault_path="./"):
        self.vault_path = vault_path
        print("-> 🧠 [Obsidian 外掛] 知識圖譜解析引擎初始化成功！")

    def parse_vault_links(self):
        """掃描所有 Markdown 檔案並解析雙向連結以建立知識圖譜"""
        md_files = glob.glob(f"{self.vault_path}*.md")
        graph_network = {}

        print(f"-> 🔍 正在掃描 {len(md_files)} 個筆記檔案...")

        for filepath in md_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 尋找 Obsidian 的雙向連結格式 [[LinkName]]
                links = re.findall(r'\[\[(.*?)\]\]', content)
                graph_network[filepath] = links

        print("\n--- 🌐 Obsidian 知識圖譜連結報告 ---")
        for node, targets in graph_network.items():
            print(f" 📄 筆記: {node}")
            print(f"    └─ 連結到的節點: {targets if targets else '無'}")
        print("------------------------------------\n")

if __name__ == "__main__":
    # 建立一個測試用的 Markdown 筆記來模擬 Vault 環境
    with open("test_note.md", "w", encoding='utf-8') as f:
        f.write("# 我的 AI 第二大腦\n這是一篇關於 [[claude-obsidian]] 與 [[Termux]] 的自動化筆記。")

    graph_plugin = ObsidianGraphPlugin()
    graph_plugin.parse_vault_links()
