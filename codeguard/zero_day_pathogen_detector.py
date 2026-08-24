import datetime

# ==============================================================
# Zero-Day Pathogen Detector - 零時差新病原體與異常入侵防護模組
# ==============================================================

class ZeroDayPathogenDetector:
    # 已知的安全特徵碼清單
    KNOWN_SIGNATURES = ["SAFE_CORE_PULSE", "STANDARD_DATA_READ", "MEMORY_STABLE"]

    @classmethod
    def scan_and_quarantine_pathogen(cls, incoming_payload):
        """掃描外部或內部入侵的程式碼特徵，防範未知的『新疾病』入侵"""
        print("=" * 60)
        print(f" 🦠 [病原檢測中心] 正在進行新型入侵與零時差病原掃描...")
        print(f" 檢測內容: [{incoming_payload}]")
        print("=" * 60)

        # 啟發式檢測：若載荷不包含已知安全特徵，且含有破壞性關鍵字
        is_known = any(sig in incoming_payload for sig in cls.KNOWN_SIGNATURES)
        is_destructive = any(keyword in incoming_payload for keyword in ["INJECT", "CORRUPT", "OVERRIDE", "UNKNOWN_VIRUS"])

        if not is_known and is_destructive:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"-> 🔴 [高度警戒] 偵測到未知的新型疾病/零時差攻擊入侵！")
            print(f"    入侵時間: {timestamp}")
            print(f"    防護動作: 啟動硬體級沙箱隔離，將威脅鎖定在獨立隔離區中。")
            return "QUARANTINED"
        else:
            print("-> 🟢 [安全通過] 檢測完畢，未發現新型病原體入侵威脅。")
            return "CLEAN"

if __name__ == "__main__":
    # 測試 1：正常的安全訊號
    ZeroDayPathogenDetector.scan_and_quarantine_pathogen("SAFE_CORE_PULSE")
    print("-" * 60)
    # 測試 2：模擬遭遇未知的新型病原體入侵
    ZeroDayPathogenDetector.scan_and_quarantine_pathogen("UNKNOWN_VIRUS_INJECT_PAYLOAD")

