import socket
import datetime

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    透過嘗試連線到外部知名伺服器（預設為 Google DNS 8.8.8.8 的 53 埠）
    來檢測當前軟體環境是否成功連線到真實世界的網際網路。
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"-> 🌐 [網路檢測 - {timestamp}] 正在測試是否連線到外部網路...")

    try:
        # 嘗試建立一個 Socket 連線
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print(f"-> [✔] 網路連線成功！當前軟體環境已連線至真實世界的網際網路。")
        return True
    except socket.error as ex:
        print(f"-> [❌] 網路連線失敗：目前無法連線至外部網路（原因: {ex}）")
        return False

if __name__ == "__main__":
    # 執行檢測函式
    is_connected = check_internet_connection()

    # 根據檢測結果提供程式邏輯上的參考
    if is_connected:
        print("-> 💡 [提示] 你的程式現在可以安全地呼叫外部網路 API 或雲端大腦服務。")
    else:
        print("-> 💡 [提示] 你的程式目前處於離線狀態，建議切換至本地模擬模式。")

