import sqlite3
import requests
import json
from collections import defaultdict

class MatrixWeb3GraphAgent:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[Web3-Graph-Agent] 正在初始化鏈上雷達與關聯圖譜分析引擎...")

    def scan_onchain_contracts(self):
        """模擬或串接公共 RPC 掃描鏈上熱門合約或空投訊號"""
        print("[On-Chain Radar] 正在向鏈上節點發送資料查詢請求 (Solana / EVM RPC)...")
        try:
            url = "https://api.llama.fi/protocols"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                protocols = res.json()
                sorted_protocols = sorted(protocols, key=lambda x: x.get('change_1d', 0) or 0, reverse=True)
                
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                added = 0
                for p in sorted_protocols[:3]:
                    name = p.get("name")
                    chain = p.get("chain")
                    tvl = p.get("tvl", 0)
                    title = f"[Web3 鏈上熱點] {name} (鏈: {chain}, TVL: ${tvl:,.0f})"
                    link = f"https://defillama.com/protocol/{p.get('slug')}"
                    
                    cursor.execute("SELECT id FROM intel_vault WHERE link = ?", (link,))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO intel_vault (source, title, link, category) VALUES (?, ?, ?, ?)",
                            ("On-Chain Radar", title, link, "Crypto & Web3")
                        )
                        added += 1
                conn.commit()
                conn.close()
                print(f"[✅ 鏈上雷達] 成功捕獲並入庫 {added} 筆鏈上高價值財富訊號！")
        except Exception as e:
            print(f"[❌ 鏈上雷達異常] {e}")

    def build_knowledge_graph(self):
        """建構輕量級矩陣關聯圖譜（分析不同情報之間的關鍵字交集）"""
        print("[Graph Engine] 正在分析智庫數據，建構跨領域知識圖譜...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT title, category FROM intel_vault")
        rows = cursor.fetchall()
        conn.close()

        category_clusters = defaultdict(list)
        for title, category in rows:
            category_clusters[category].append(title)

        print("\n=== 🧠 矩陣智慧知識圖譜分析報告 ===")
        for cat, titles in category_clusters.items():
            print(f"🔗 核心領域集群: [{cat}] (包含 {len(titles)} 個節點)")
            for t in titles[:2]:
                print(f"     ├─ 結點: {t[:50]}...")
        print("======================================\n")

    def run_agent(self):
        self.scan_onchain_contracts()
        self.build_knowledge_graph()

if __name__ == "__main__":
    agent = MatrixWeb3GraphAgent()
    agent.run_agent()
import sqlite3
import requests
import json
from collections import defaultdict

class MatrixWeb3GraphAgent:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[Web3-Graph-Agent] 正在初始化鏈上雷達與關聯圖譜分析引擎...")

    def scan_onchain_contracts(self):
        """模擬或串接公共 RPC 掃描鏈上熱門合約或空投訊號"""
        print("[On-Chain Radar] 正在向鏈上節點發送資料查詢請求 (Solana / EVM RPC)...")
        try:
            url = "https://api.llama.fi/protocols"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                protocols = res.json()
                sorted_protocols = sorted(protocols, key=lambda x: x.get('change_1d', 0) or 0, reverse=True)
                
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                added = 0
                for p in sorted_protocols[:3]:
                    name = p.get("name")
                    chain = p.get("chain")
                    tvl = p.get("tvl", 0)
                    title = f"[Web3 鏈上熱點] {name} (鏈: {chain}, TVL: ${tvl:,.0f})"
                    link = f"https://defillama.com/protocol/{p.get('slug')}"
                    
                    cursor.execute("SELECT id FROM intel_vault WHERE link = ?", (link,))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO intel_vault (source, title, link, category) VALUES (?, ?, ?, ?)",
                            ("On-Chain Radar", title, link, "Crypto & Web3")
                        )
                        added += 1
                conn.commit()
                conn.close()
                print(f"[✅ 鏈上雷達] 成功捕獲並入庫 {added} 筆鏈上高價值財富訊號！")
        except Exception as e:
            print(f"[❌ 鏈上雷達異常] {e}")

    def build_knowledge_graph(self):
        """建構輕量級矩陣關聯圖譜（分析不同情報之間的關鍵字交集）"""
        print("[Graph Engine] 正在分析智庫數據，建構跨領域知識圖譜...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT title, category FROM intel_vault")
        rows = cursor.fetchall()
        conn.close()

        category_clusters = defaultdict(list)
        for title, category in rows:
            category_clusters[category].append(title)

        print("\n=== 🧠 矩陣智慧知識圖譜分析報告 ===")
        for cat, titles in category_clusters.items():
            print(f"🔗 核心領域集群: [{cat}] (包含 {len(titles)} 個節點)")
            for t in titles[:2]:
                print(f"     ├─ 結點: {t[:50]}...")
        print("======================================\n")

    def run_agent(self):
        self.scan_onchain_contracts()
        self.build_knowledge_graph()

if __name__ == "__main__":
    agent = MatrixWeb3GraphAgent()
    agent.run_agent()
