import sys
from core import GenesisCore

def main():
    print("==========================================")
    print("  Genesis Core Eternity - 自動演進系統啟動 ")
    print("==========================================")
    
    try:
        core = GenesisCore()
        core.execute_cycle()
        print("[SUCCESS] 演進週期執行成功！")
    except Exception as e:
        print(f"[ERROR] 執行過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
