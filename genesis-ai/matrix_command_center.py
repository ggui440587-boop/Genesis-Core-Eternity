import sqlite3
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import print as rprint

console = Console()

class MatrixCommandCenter:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name

    def render_dashboard(self):
        """渲染高顏值終端機動態戰情看板"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 統計數據
        cursor.execute("SELECT COUNT(*) FROM intel_vault")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM intel_vault GROUP BY category")
        category_stats = cursor.fetchall()
        
        # 取得最新 8 筆情報
        cursor.execute("SELECT source, title, category, created_at FROM intel_vault ORDER BY id DESC LIMIT 8")
        recent_items = cursor.fetchall()
        conn.close()

        console.clear()
        
        # 標題面板
        console.print(Panel.fit(
            "[bold cyan]🚀 楊哲熙的 Termux 數位自動化作戰矩陣[/bold cyan]\n[yellow]狀態：全天候後台全速運轉中 | 戰情看板已啟動[/yellow]",
            border_style="bright_blue"
        ))

        # 統計資訊表格
        stat_table = Table(title="📊 智庫數據總覽", border_style="green")
        stat_table.add_column("總情報數", justify="center", style="bold magenta")
        for cat, _ in category_stats:
            stat_table.add_column(cat, justify="center", style="cyan")
            
        row_data = [str(total_count)]
        for _, count in category_stats:
            row_data.append(str(count))
        stat_table.add_row(*row_data)
        console.print(stat_table)

        # 最新情報戰利品表格
        item_table = Table(title="🔥 最新捕獲的高價值戰利品", border_style="yellow")
        item_table.add_column("分類", style="cyan", width=18)
        item_table.add_column("標題 / 摘要", style="white", width=55)
        item_table.add_column("來源通道", style="dim", width=20)

        for source, title, category, created_at in recent_items:
            item_table.add_row(category, title[:50] + "...", source)
            
        console.print(item_table)
        console.print("\n[bold green]💡 提示：[/bold green] 您可以輸入 [cyan]python matrix_command_center.py search [關鍵字][/cyan] 來進行智庫智慧檢索！\n")

    def search_vault(self, keyword):
        """本地智庫智慧檢索功能"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, link, category, created_at FROM intel_vault WHERE title LIKE ? OR category LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        results = cursor.fetchall()
        conn.close()

        console.print(f"\n[bold yellow]🔍 針對「{keyword}」的本地智庫檢索結果：[/bold yellow]\n")
        if not results:
            console.print("[red]沒有找到相符的情報標的。[/red]")
            return

        table = Table(border_style="magenta")
        table.add_column("分類", style="cyan")
        table.add_column("標題", style="white")
        table.add_column("直達通道", style="blue")

        for title, link, category, _ in results:
            table.add_row(category, title[:50], link)
        console.print(table)

if __name__ == "__main__":
    center = MatrixCommandCenter()
    if len(sys.argv) > 1 and sys.argv[1] == "search" and len(sys.argv) > 2:
        center.search_vault(sys.argv[2])
    else:
        center.render_dashboard()

