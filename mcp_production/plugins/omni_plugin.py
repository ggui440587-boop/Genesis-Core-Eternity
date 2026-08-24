import os
import aiohttp
from .base import BasePlugin

class Plugin(BasePlugin):
    async def execute(self):
        # 從安全環境變數讀取金鑰，絕不寫死
        groq_key = os.getenv("GROQ_KEY")
        github_token = os.getenv("GITHUB_TOKEN")
        
        headers_groq = {"Authorization": f"Bearer {groq_key}"}
        headers_mcp = {"Authorization": f"token {github_token}", "X-MCP-Protocol-Version": "2026.08"}
        
        async with aiohttp.ClientSession() as session:
            # 1. 測試 Groq 狀態
            try:
                async with session.get("https://api.groq.com/openai/v1/models", headers=headers_groq, timeout=5) as res:
                    print(f"[Groq 插件] 連線狀態: {res.status}")
            except Exception as e:
                print(f"[Groq 插件] 請求受阻: {e}")

            # 2. 測試 MCP / GitHub 節點狀態
            try:
                async with session.get("https://api.github.com/user", headers=headers_mcp, timeout=5) as res:
                    print(f"[MCP 節點插件] 連線狀態: {res.status}")
            except Exception as e:
                print(f"[MCP 節點插件] 請求受阻: {e}")

