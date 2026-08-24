import os
import subprocess
import aiohttp
import random
from .base import BasePlugin

class Plugin(BasePlugin):
    processed_count = 0
    domains = [
        "領域一：AI 智慧代理與工作流自動化 (Autonomous Agents)",
        "領域二：大數據與即時資料分析 (Big Data Analytics)",
        "領域三：資安防護與漏洞檢測 (Cybersecurity Assessment)",
        "領域四：演算法優化與高效能計算 (Algorithm Optimization)",
        "領域五：物聯網與邊緣計算工具 (IoT Edge Computing)"
    ]

    async def execute(self):
        if Plugin.processed_count >= len(Plugin.domains):
            print("\n🛑 [工坊公告]: 5 個跨領域的創新研發專案已全部完成！")
            return

        current_domain = Plugin.domains[Plugin.processed_count]
        print(f"\n================ [跨領域知識轉化與創新研發 (進度: {Plugin.processed_count+1}/5)] ================")
        print(f"🎯 當前鎖定研發領域: 【{current_domain}】")
        
        github_token = os.getenv("GITHUB_TOKEN")
        groq_key = os.getenv("GROQ_KEY")
        
        headers_github = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with aiohttp.ClientSession() as session:
            repos_url = "https://api.github.com/user/repos?per_page=15&sort=updated"
            target_repo_name = None
            
            try:
                async with session.get(repos_url, headers=headers_github, timeout=6) as res:
                    if res.status == 200:
                        repos = await res.json()
                        if len(repos) > Plugin.processed_count:
                            target_repo_name = repos[Plugin.processed_count]["name"]
                        elif repos:
                            target_repo_name = repos[0]["name"]
                        print(f"📦 對應雲端倉庫: 【{target_repo_name}】")
            except Exception as e:
                print(f"⚠️ 檢索異常: {e}")

            if not target_repo_name:
                return

            print("🤖 [AI 知識轉化與研發中]: 正在透過 Groq 生成該領域核心代碼...")
            
            research_code = f"# 領域研究專案: {current_domain}\nimport sys\n\ndef main():\n    print('Initializing {current_domain} Research Module...')\n\nif __name__ == '__main__':\n    main()"
            
            if groq_key:
                groq_headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                prompt_content = f"請為專案 '{target_repo_name}' 在『{current_domain}』領域寫一個完整的 Python 程式 main.py。必須包含核心邏輯與完整註解，絕對不要有 markdown 標籤或廢話。"
                
                groq_payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt_content}],
                    "temperature": 0.5
                }
                # 確保網址絕對乾淨無多餘字元
                groq_url = "https://api.groq.com/openai/v1/chat/completions"
                try:
                    async with session.post(groq_url, headers=groq_headers, json=groq_payload, timeout=20) as g_res:
                        if g_res.status == 200:
                            g_data = await g_res.json()
                            raw_content = g_data["choices"][0]["message"]["content"]
                            research_code = raw_content.replace("```python", "").replace("```", "").strip()
                            print("✨ [創新研發代碼生成成功]！")
                        else:
                            print(f"⚠️ Groq API 回應狀態碼: {g_res.status}")
                except Exception as ge:
                    print(f"⚠️ 生成異常: {ge}")

            print("\n--------------------------------------------------")
            print(f"📌 準備更新倉庫: 【{target_repo_name}】")
            print("📝 【代碼預覽】:")
            print("--------------------------------------------------")
            print(research_code[:500] + "\n... (以下略)")
            print("--------------------------------------------------")

            choice = input("👉 是否確認上架此內容？ (y/N): ").strip().lower()
            if choice != 'y':
                print("🚫 [手動攔截]: 您跳過了此倉庫。")
                return

            project_dir = f"workspace_research_{target_repo_name}"
            os.makedirs(project_dir, exist_ok=True)
            
            with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
                f.write(research_code)
                
            with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write("requests>=2.31.0\naiohttp>=3.8.0")
                
            with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
                f.write(f"# {target_repo_name}\n\n> 🔬 Cross-Domain Research: {current_domain}\n\n## 執行方式\n```bash\npython main.py\n```")

            # 修正 Git Push 網址格式與驗證
            repo_clone_url = f"https://{github_token}@github.com/ggui440587-boop/{target_repo_name}.git"
            
            print(f"🚀 [執行上架]: 正在推送至雲端...")
            try:
                subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "AI-Agent"], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "agent@ai.local"], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"Update {current_domain}"], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "branch", "-M", "main"], cwd=project_dir, check=True, capture_output=True)
                subprocess.run(["git", "remote", "add", "origin", repo_clone_url], cwd=project_dir, check=True, capture_output=True)
                
                # 使用 force push 確保覆蓋順利
                push_res = subprocess.run(["git", "push", "-f", "origin", "main"], cwd=project_dir, capture_output=True, text=True, timeout=20)
                
                if push_res.returncode == 0:
                    Plugin.processed_count += 1
                    print(f"🎉 [上架成功]: 倉庫 【{target_repo_name}】 已更新！(總進度: {Plugin.processed_count}/5)")
                else:
                    print(f"⚠️ Git 推送失敗，詳細錯誤: {push_res.stderr}")
            except Exception as se:
                print(f"⚠️ 執行過程異常: {se}")

        print("====================================================================\n")

