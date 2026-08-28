import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live

console = Console()

def generate_dashboard():
    # 建立主排版
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )

    # 1. 頂部標題區
    layout["header"].update(Panel("🚀 ARGONA - 終極自動化多代理人監控儀表板", style="bold white on blue"))

    # 2. 中間數據表格區
    table = Table(title="即時系統代理人狀態", expand=True)
    table.add_column("Agent ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Role", style="magenta")
    table.add_column("Status", justify="right", style="green")
    table.add_column("Performance", justify="right", style="yellow")

    table.add_row("Grok-01", "數據檢索與過濾", "🟢 運行中", "+43.0%")
    table.add_row("Kimi-K3", "邏輯分析與合成", "🟢 運行中", "+89.5%")
    table.add_row("Core-Engine", "背景基因融合", "🟡 待命", "0.0%")

    layout["body"].update(Panel(table, title="Live Metrics"))

    # 3. 底部狀態區
    layout["footer"].update(Panel("💡 提示：按 Ctrl + C 可以安全關閉此儀表板畫面。", style="dim"))

    return layout

if __name__ == "__main__":
    try:
        with Live(generate_dashboard(), refresh_per_second=4, screen=True) as live:
            while True:
                time.sleep(1)
                # 這裡可以動態更新畫面資料
                live.update(generate_dashboard())
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 使用者已手動關閉儀表板畫面。[/red]")
