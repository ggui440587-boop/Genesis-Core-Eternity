import time

class InMemoryCachePlugin:
    def __init__(self):
        self.storage = {}
        print("-> ⚡ [記憶體快取外掛] 初始化成功！支援 TTL (有效期限) 快取機制。")

    def set(self, key, value, ttl_seconds=60):
        """將資料存入快取，並設定過期秒數"""
        expire_time = time.time() + ttl_seconds
        self.storage[key] = {"value": value, "expire": expire_time}

    def get(self, key):
        """取得快取資料，若已過期則自動清除並回傳 None"""
        if key not in self.storage:
            return None
        
        item = self.storage[key]
        if time.time() > item["expire"]:
            del self.storage[key]
            return None
        
        return item["value"]

if __name__ == "__main__":
    cache = InMemoryCachePlugin()
    cache.set("test_key", "Hello Cache", ttl_seconds=2)
    print("Immediate Get:", cache.get("test_key"))
    time.sleep(3)
    print("After Expired Get:", cache.get("test_key"))
