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

# 導入我們之前的真實程式碼橋接模組
from real_code_bridge import RealCodeBridge

logging.basicConfig(
    filename="mutant_alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class MutantFactory:
    def __init__(self, output_file="genesis_core_eternity.py"):
        self.output_file = output_file
        self.sources_file = "sources.json"
        self.queue = asyncio.Queue()
        
        self.status = "突變工廠就緒"
        self.total_lines = 0
        self.processed_tasks = 0
        self.mutation_count = 0

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
            self.status = f"突變 Worker #{worker_id} 正在融合: {name}"
            
            try:
                loop = asyncio.get_running_loop()
                def download():
                    import urllib.request
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=8) as response:
                        return response.read().decode('utf-8')
                
                code_content = await loop.run_in_executor(None, download)
                
                # 隨機突變引擎：隨機產生一組突變基因標籤
                mutation_id = random.randint(1000, 9999)
                self.mutation_count += 1
                
                filtered_lines = [line for line in code_content.splitlines() if "__future__" not in line]
                safe_code = "\n".join(filtered_lines)
                
                clean_code = f"\n# === [MUTANT GENE START: {name} | ID: {mutation_id}] ===\n" + safe_code + f"\n# === [MUTANT GENE END: {name}] ===\n"
                
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(clean_code)
                
                self.processed_tasks += 1
            except Exception as e:
                logging.error(f"突變融合失敗 [{name}]: {e}")
            
            self.queue.task_done()

    def _git_sync(self):
        self.status = "正在同步突變成果至遠端 GitHub..."
        try:
            subprocess.run(["git", "add", self.output_file], capture_output=True, check=True)
            commit_msg = f"Mutant auto-sync: {datetime.datetime.now().strftime('%H:%M:%S')}"
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

        layout["header"].update(Panel("🧬 隨機突變與真實模組融合工廠 - 戰情室", style="bold white on blue"))

        table = Table(title="即時突變與系統效能監控", expand=True)
        table.add_column("監控指標", style="cyan")
        table.add_column("狀態數值", style="magenta")

        table.add_row("系統狀態", f"[yellow]{self.status}[/yellow]")
        table.add_row("已完成突變任務", f"{self.processed_tasks} 個")
        table.add_row("隨機突變總次數", f"[green]{self.mutation_count} 次[/green]")
        table.add_row("核心總行數", f"{self.total_lines} 行")

        layout["body"].update(Panel(table, title="Mutant Telemetry"))
        layout["footer"].update(Panel("💡 提示：已啟動隨機基因突變引擎。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

async def run_mutant_cycle():
    factory = MutantFactory()
    
    with open(factory.output_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# Mutant Flagship Core\n\n")

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
    factory.status = "本輪隨機突變循環圓滿完成！"

if __name__ == "__main__":
    interval_seconds = 30
    try:
        console.print("[green]-> 🧬 啟動隨機突變自動化融合工廠...[/green]")
        while True:
            asyncio.run(run_mutant_cycle())
            time.sleep(1)
            console.print(f"[cyan]-> 💤 本輪結束，進入休眠 {interval_seconds} 秒...[/cyan]")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 隨機突變工廠已被使用者手動終止。[/red]")
