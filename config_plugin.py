class ConfigPlugin:
    def get(self, key):
        return {"version": "16.0", "sleep_interval": 10, "max_retries": 3}.get(key)
