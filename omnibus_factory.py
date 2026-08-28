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
    filename="omnibus_alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class OmnibusFactory:
    def __init__(self, output_file="genesis_core_eternity.py", db_file="fusion_history.db"):
        self.output_file = output_file
        self.db_file = db_file
        self.sources_file = "sources.json"
        self.queue = asyncio.Queue()
        
        self.status = "系統全方位待命"
        self.total_lines = 0
        self.processed_tasks = 0
        self.failed_tasks = 0
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS omnibus_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_lines INTEGER,
                processed INTEGER,
                failed INTEGER,
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
            self.status = f"Worker #{worker_id} 正在安全抓取: {name}"
            
            success = False
            code_content = ""
            
            # 內建 3 次指數退避重試機制 (Exponential Backoff Retry)
            for attempt in range(3):
                try:
                    loop = asyncio.get_running_loop()
                    def download():
                        import urllib.request
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=8) as response:
                            return response.read().decode('utf-8')
                    
                    code_content = await loop.run_in_executor(None, download)
                    success = True
                    break
                except Exception as e:
                    if attempt == 2:
                        logging.error(f"抓取最終失敗 [{name}]: {e}")
                    await asyncio.sleep(2 ** attempt)

            if success:
                filtered_lines = [line for line in code_content.splitlines() if "__future__" not in line]
                safe_code_content = "\n".join(filtered_lines)
                clean_code = f"\n# === [GENE START: {name}] ===\n" + safe_code_content + f"\n# === [GENE END: {name}] ===\n"
                
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(clean_code)
                
                self.processed_tasks += 1
            else:
                self.failed_tasks += 1

            self.queue.task_done()

    def _git_sync(self):
        self.status = "正在同步至遠端 GitHub..."
        try:
            subprocess.run(["git", "add", self.output_file], capture_output=True, check=True)
            commit_message = f"Omnibus full auto-sync: {datetime.datetime.now().strftime('%H:%M:%S')}"
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

        layout["header"].update(Panel("🚀 全方位旗艦級自動化融合工廠 - 終極戰情室", style="bold white on blue"))

        table = Table(title="全方位系統效能與防護監控", expand=True)
        table.add_column("監控指標", style="cyan")
        table.add_column("狀態數值", style="magenta")

        table.add_row("系統狀態", f"[yellow]{self.status}[/yellow]")
        table.add_row("成功處理任務", f"[green]{self.processed_tasks}[/green] 個")
        table.add_row("失敗重試阻斷", f"[red]{self.failed_tasks}[/red] 個")
        table.add_row("核心總行數", f"{self.total_lines} 行")

        layout["body"].update(Panel(table, title="Omnibus Telemetry"))
        layout["footer"].update(Panel("💡 提示：已啟動重試機制與安全防護。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

async def run_omnibus_cycle():
    factory = OmnibusFactory()
    
    with open(factory.output_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# Omnibus Flagship Core\n\n")

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
    
    # 紀錄至 SQLite
    conn = sqlite3.connect(factory.db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO omnibus_logs (timestamp, total_lines, processed, failed, status) VALUES (?, ?, ?, ?, ?)",
        (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), factory.total_lines, factory.processed_tasks, factory.failed_tasks, "SUCCESS")
    )
    conn.commit()
    conn.close()

    factory.status = "全方位本輪循環圓滿完成！"

if __name__ == "__main__":
    interval_seconds = 30
    try:
        console.print("[green]-> 🚀 啟動全方位旗艦自動化循環工廠...[/green]")
        while True:
            asyncio.run(run_omnibus_cycle())
            time.sleep(1)
            console.print(f"[cyan]-> 💤 全方位本輪結束，進入休眠 {interval_seconds} 秒...[/cyan]")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 全方位循環工廠已被使用者手動終止。[/red]")
