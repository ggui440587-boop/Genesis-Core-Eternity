def process(text: str) -> str:
    print(f"[A 執行] 接收到: {text}")
    return text.upper()

if __name__ == "__main__":
    # 給右側野生盲撞用的標準輸入輸出
    import sys
    data = sys.stdin.read().strip()
    print(data.upper())
