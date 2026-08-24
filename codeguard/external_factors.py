import socket
import datetime

# ==============================================================
# External Factors Module - 外部環境與網路狀態監控模組
# ==============================================================

class ExternalFactorsModule:
    @staticmethod
    def check_external_environment():
        """檢查外部因素：例如對外網路連線狀態與當前時間環境"""
        print("=" * 50)
        print(" 🌐 [外部因素] 正在檢測外部環境與網路連線狀態...")
        print("=" * 50)

        # 檢查外部網路連線 (嘗試連接常見的公用 DNS 8.8.8.8)
        is_connected = False
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            is_connected = True
            print("-> [網路狀態] 🟢 外部網路連線正常，具備通訊能力。")
        except OSError:
            print("-> [網路狀態] 🔴 外部網路無法連線，目前處於離線/孤立環境。")

        # 取得當前時間外部因素
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"-> [時間環境] ⏰ 當前外部時間標記: {current_time}")

        return {
            "network_online": is_connected,
            "timestamp": current_time
        }

if __name__ == "__main__":
    ExternalFactorsModule.check_external_environment()

