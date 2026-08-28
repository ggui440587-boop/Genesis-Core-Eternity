import os
import json
import asyncio
import datetime
import subprocess
import sqlite3
import time
import logging

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live

logging.basicConfig(
    filename="alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class FlagshipFactory:
    def __init__(self, output_file="genesis_core_eternity.py", db_file="fusion_history.db"):
        self.output_file = output_file
        self.db_file = db_file
        self.sources_file = "sources.json"
        self.queue = asyncio.Queue()
        
        self.status = "系統待命"
        self.total_lines = 0
        self.processed_tasks = 0
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_lines INTEGER,
                gene_count INTEGER,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

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
            self.status = f"Worker #{worker_id} 正在抓取: {name}"
            
            try:
                loop = asyncio.get_running_loop()
                def download():
                    import urllib.request
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=8) as response:
                        return response.read().decode('utf-8')
                
                code_content = await loop.run_in_executor(None, download)
                
                # 過濾掉遠端程式碼中可能夾帶的 __future__ 宣告，避免語法崩潰
                filtered_lines = []
                for line in code_content.splitlines():
                    if "__future__" not in line:
                        filtered_lines.append(line)
                safe_code_content = "\n".join(filtered_lines)

                clean_code = f"\n# === [GENE START: {name}] ===\n" + safe_code_content + f"\n# === [GENE END: {name}] ===\n"
                
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
            commit_message = f"Flagship safe auto-sync: {datetime.datetime.now().strftime('%H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, check=True)
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

        layout["header"].update(Panel("🚀 旗艦級全自動循環佇列工廠 - 戰情室", style="bold white on blue"))

        table = Table(title="即時系統效能與任務監控", expand=True)
        table.add_column("監控指標", style="cyan")
        table.add_column("狀態數值", style="magenta")

        table.add_row("系統狀態", f"[yellow]{self.status}[/yellow]")
        table.add_row("已處理任務數", f"{self.processed_tasks} 個")
        table.add_row("核心總行數", f"{self.total_lines} 行")

        layout["body"].update(Panel(table, title="Safe Queue Telemetry"))
        layout["footer"].update(Panel("💡 提示：系統正以安全過濾模式運行。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

async def run_cycle():
    factory = FlagshipFactory()
    
    with open(factory.output_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# Flagship Safe Core\n\n")

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
    factory.status = "本輪循環圓滿完成！"

if __name__ == "__main__":
    interval_seconds = 30
    try:
        console.print("[green]-> 🚀 啟動安全過濾版全自動循環工廠...[/green]")
        while True:
            asyncio.run(run_cycle())
            time.sleep(1)
            console.print(f"[cyan]-> 💤 本輪結束，進入休眠 {interval_seconds} 秒...[/cyan]")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 全自動循環工廠已被使用者手動終止。[/red]")
