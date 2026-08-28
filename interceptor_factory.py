import os
import json
import asyncio
import datetime
import subprocess
import random
import time
import logging

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live

logging.basicConfig(
    filename="interceptor_alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class InterceptorFactory:
    def __init__(self, output_file="genesis_core_eternity.py"):
        self.output_file = output_file
        self.sources_file = "sources.json"
        self.queue = asyncio.Queue()
        
        self.status = "攔截防護系統就緒"
        self.total_lines = 0
        self.processed_tasks = 0
        self.intercepted_errors = 0
        self.last_error_msg = "無"

    def load_sources(self):
        if not os.path.exists(self.sources_file):
            return [{"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"}]
        try:
            with open(self.sources_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    async def producer(self):
        sources = self.load_sources()
        for gene in sources:
            await self.queue.put(gene)

    async def consumer(self, worker_id):
        while True:
            gene = await self.queue.get()
            name = gene.get("name")
            url = gene.get("url")
            self.status = f"攔截 Worker #{worker_id} 正在處理: {name}"
            
            try:
                loop = asyncio.get_running_loop()
                def download():
                    import urllib.request
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=8) as response:
                        return response.read().decode('utf-8')
                
                code_content = await loop.run_in_executor(None, download)
                
                mutation_id = random.randint(1000, 9999)
                filtered_lines = [line for line in code_content.splitlines() if "__future__" not in line]
                safe_code = "\n".join(filtered_lines)
                
                clean_code = f"\n# === [INTERCEPTED GENE: {name} | ID: {mutation_id}] ===\n" + safe_code + f"\n# === [END GENE] ===\n"
                
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(clean_code)
                
                self.processed_tasks += 1
            except Exception as e:
                self.intercepted_errors += 1
                self.last_error_msg = str(e)[:40]
                logging.error(f"攔截到例外錯誤 [{name}]: {e}")
            
            self.queue.task_done()

    def _git_sync(self):
        self.status = "正在同步至遠端 GitHub..."
        try:
            subprocess.run(["git", "add", self.output_file], capture_output=True, check=True)
            commit_msg = f"Interceptor auto-sync: {datetime.datetime.now().strftime('%H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, check=True)
            subprocess.run(["git", "push"], capture_output=True, check=True, timeout=15)
        except Exception as e:
            logging.error(f"Git 同步失敗: {e}")

    def build_ui(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )

        layout["header"].update(Panel("🛡️ 錯誤攔截與日誌回溯工廠 - 戰情室", style="bold white on blue"))

        table = Table(title="即時系統防護與健康度監控", expand=True)
        table.add_column("監控指標", style="cyan")
        table.add_column("狀態數值", style="magenta")

        table.add_row("系統狀態", f"[yellow]{self.status}[/yellow]")
        table.add_row("成功處理任務", f"{self.processed_tasks} 個")
        table.add_row("已攔截異常數", f"[red]{self.intercepted_errors} 次[/red]")
        table.add_row("最近錯誤摘要", f"[dim red]{self.last_error_msg}[/dim red]")
        table.add_row("核心總行數", f"{self.total_lines} 行")

        layout["body"].update(Panel(table, title="Interceptor Telemetry"))
        layout["footer"].update(Panel("💡 提示：已啟動錯誤攔截器。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

async def run_interceptor_cycle():
    factory = InterceptorFactory()
    
    with open(factory.output_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# Interceptor Flagship Core\n\n")

    await factory.producer()
    workers = [asyncio.create_task(factory.consumer(i)) for i in range(2)]
    
    await factory.queue.join()
    for w in workers:
        w.cancel()

    factory.status = "正在執行編譯與 Git 同步..."
    
    if os.path.exists(factory.output_file):
        with open(factory.output_file, "r", encoding="utf-8") as f:
            factory.total_lines = len(f.readlines())

    factory._git_sync()
    factory.status = "本輪攔截防護循環圓滿完成！"

if __name__ == "__main__":
    interval_seconds = 30
    try:
        console.print("[green]-> 🛡️ 啟動錯誤攔截自動化融合工廠...[/green]")
        while True:
            asyncio.run(run_interceptor_cycle())
            time.sleep(1)
            console.print(f"[cyan]-> 💤 本輪結束，進入休眠 {interval_seconds} 秒...[/cyan]")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 錯誤攔截工廠已被使用者手動終止。[/red]")
