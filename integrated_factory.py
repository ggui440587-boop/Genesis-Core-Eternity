import os
import json
import asyncio
import datetime
import subprocess
import time
import logging

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live

# 導入我們剛剛驗證成功的知識庫引擎
from knowledge_db_engine import KnowledgeDatabaseEngine

logging.basicConfig(
    filename="integrated_alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class IntegratedFactory:
    def __init__(self, output_file="genesis_core_eternity.py"):
        self.output_file = output_file
        self.sources_file = "sources.json"
        self.queue = asyncio.Queue()
        self.db_engine = KnowledgeDatabaseEngine(db_name="knowledge_matrix.db")
        
        self.status = "系統模組化就緒"
        self.total_lines = 0
        self.processed_tasks = 0

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
            self.status = f"整合 Worker #{worker_id} 正在處理: {name}"
            
            try:
                loop = asyncio.get_running_loop()
                def download():
                    import urllib.request
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=8) as response:
                        return response.read().decode('utf-8')
                
                code_content = await loop.run_in_executor(None, download)
                filtered_lines = [line for line in code_content.splitlines() if "__future__" not in line]
                safe_code = "\n".join(filtered_lines)
                
                clean_code = f"\n# === [GENE START: {name}] ===\n" + safe_code + f"\n# === [GENE END: {name}] ===\n"
                
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(clean_code)
                
                self.processed_tasks += 1
            except Exception as e:
                logging.error(f"抓取失敗 [{name}]: {e}")
            
            self.queue.task_done()

    def _git_sync(self):
        self.status = "正在同步至遠端 GitHub..."
        try:
            subprocess.run(["git", "add", self.output_file], capture_output=True, check=True)
            commit_msg = f"Integrated auto-sync: {datetime.datetime.now().strftime('%H:%M:%S')}"
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

        layout["header"].update(Panel("🧬 知識庫整合型自動化融合工廠 - 戰情室", style="bold white on blue"))

        table = Table(title="即時系統運作監控", expand=True)
        table.add_column("監控指標", style="cyan")
        table.add_column("狀態數值", style="magenta")

        table.add_row("系統狀態", f"[yellow]{self.status}[/yellow]")
        table.add_row("已處理任務", f"{self.processed_tasks} 個")
        table.add_row("核心總行數", f"{self.total_lines} 行")

        layout["body"].update(Panel(table, title="Integrated Telemetry"))
        layout["footer"].update(Panel("💡 提示：已成功結合資料庫引擎。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

async def run_integrated_cycle():
    factory = IntegratedFactory()
    
    with open(factory.output_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# Integrated Core\n\n")

    await factory.producer()
    workers = [asyncio.create_task(factory.consumer(i)) for i in range(2)]
    
    await factory.queue.join()
    for w in workers:
        w.cancel()

    factory.status = "正在寫入知識庫與 Git 同步..."
    
    if os.path.exists(factory.output_file):
        with open(factory.output_file, "r", encoding="utf-8") as f:
            factory.total_lines = len(f.readlines())

    # 透過我們的知識庫引擎寫入執行紀要
    factory.db_engine.insert_record("FactoryCycle", {
        "total_lines": factory.total_lines,
        "processed_tasks": factory.processed_tasks,
        "status": "SUCCESS"
    })

    factory._git_sync()
    factory.status = "本輪整合循環圓滿完成！"

if __name__ == "__main__":
    interval_seconds = 30
    try:
        console.print("[green]-> 🚀 啟動知識庫整合型自動化工廠...[/green]")
        while True:
            asyncio.run(run_integrated_cycle())
            time.sleep(1)
            console.print(f"[cyan]-> 💤 本輪結束，進入休眠 {interval_seconds} 秒...[/cyan]")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 整合工廠已被使用者手動終止。[/red]")
