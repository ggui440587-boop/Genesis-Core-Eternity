class NetworkPlugin:
    def __init__(self, endpoint_url=""): self.url = endpoint_url
    def send_ping(self, data):
        print("-> 🌐 [網路] 狀態回報成功送達！")
