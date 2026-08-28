import sqlite3
import os
import time
from datetime import datetime

DB_NAME = "fusion_hub.db"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_minimal_floor():
    if not os.path.exists(DB_NAME):
        time.sleep(2)
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT SUM(quantity) FROM imperial_treasury")
        gold = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(citizens_count), SUM(slaves_count) FROM empire_domains")
        pop = cursor.fetchone()
        c_num = pop[0] or 0
        s_num = pop[1] or 0
    except:
        gold, c_num, s_num = 0, 0, 0

    clear_screen()
    print("┌────────────────────────────────────────┐")
    print(f"│ 👑 EMPIRE FLOOR   {datetime.now().strftime('%H:%M:%S')}   LIVE 🟢│")
    print("├────────────────────────────────────────┤")
    print(f"│ 💰 GOLD: {gold:<8} 👥 CITIZEN: {c_num:<6} │")
    print(f"│ ⛓️ SLAVE: {s_num:<8} ⚡ STATUS: SECURE    │")
    print("└────────────────────────────────────────┘")
    print()
    print("  [ 👨‍💼 商會 ]      [ 👨‍🌾 拓荒 ]      [ ⛪ 教會 ]      [ 🕵️ 暗部 ]")
    print("    ACTIVE          MINING          BLESSED         WATCHING")
    print()
    print("──────────────────────────────────────────")
    print(" (每 3 秒更新 | Ctrl+C 退出)")
    conn.close()

if __name__ == "__main__":
    try:
        while True:
            render_minimal_floor()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n已退出。")

