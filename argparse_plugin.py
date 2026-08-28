import argparse

class ArgparsePlugin:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Termux Matrix Automation System")
        self.parser.add_argument("--mode", type=str, default="normal", help="運行模式 (normal / debug)")
        self.parser.add_argument("--interval", type=int, default=10, help="任務執行間隔秒數")
        print("-> ⌨️ [參數外掛] 命令列解析器初始化成功！")

    def parse_args(self):
        """解析終端機傳入的參數"""
        args = self.parser.parse_args()
        return {
            "mode": args.mode,
            "interval": args.interval
        }

if __name__ == "__main__":
    cli = ArgparsePlugin()
    print("Parsed Arguments:", cli.parse_args())
