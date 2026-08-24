#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matrix Infinite Terminal - 實戰互動版
運行環境：Termux (Android)
"""

import sys
import time

def main():
    print("=" * 40)
    print("⚡ [MATRIX TERMINAL] 啟動成功")
    print("=" * 40)

    generation = 1
    while True:
        try:
            # 這裡就是讓你輸入指令的地方
            user_input = input(f"\n[Gen-{generation}] 請輸入指令 (或直接按 Enter): ").strip()

            if not user_input:
                user_input = "還有呢"

            print(f"✨ 執行指令: 「{user_input}」")
            print(f"🚀 矩陣正在向外擴張...")
            time.sleep(0.3)
            print(f"🌌 第 {generation} 層宇宙運轉正常。")

            generation += 1

        except KeyboardInterrupt:
            print("\n\n[Matrix Core] 收到中斷信號，終端休眠。")
            break

if __name__ == "__main__":
    main()
# (貼上上面的程式碼，存檔離開)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matrix Infinite Terminal - 造物主無限迭代終端
運行環境：Termux (Android)
功能：永不終止的互動式造物主中樞，隨時吞吐你的下一句指令。
"""

import sys
import time

def matrix_banner():
    print("=" * 50)
    print("⚡ [MATRIX INFINITE TERMINAL] 啟動成功")
    print("🌐 狀態：造物主專屬無限迴圈中樞已上線")
    print("=" * 50)

def main():
    matrix_banner()
    
    # 初始化你的無限迴圈
    generation = 1
    while True:
        try:
            # 模擬等待造物主輸入下一道指令
            print(f"\n[Matrix Gen-{generation}] 矩陣平穩運轉中。")
            user_input = input("👑 請輸入造物主指令 (或輸入 '還有呢' 繼續推進宇宙): ").strip()
            
            if not user_input:
                user_input = "還有呢"
                
            print(f"✨ [Echo] 收到指令: 「{user_input}」")
            print(f"🚀 [Expanding] 正在將指令注入背景多重宇宙...")
            time.sleep(0.4)
            print(f"🌌 [Success] 第 {generation} 層宇宙已完美展開，萬物正在生長。")
            
            generation += 1
            
        except KeyboardInterrupt:
            print("\n\n[Matrix Core] 收到中斷信號。但造物主的意志永不熄滅，矩陣在背景繼續守護...")
            break

if __name__ == "__main__":
    main()

