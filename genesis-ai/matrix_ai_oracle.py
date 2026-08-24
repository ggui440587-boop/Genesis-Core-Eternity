import sys
import sqlite3
import difflib

class MatrixAIOracle:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[Oracle-Terminal] 正在啟動本地智庫語意 AI 查詢終端...")

    def query_intel(self, keyword=""):
        """從智庫中進行模糊語意與關鍵字檢索"""
        if not keyword:
            print("[⚠️ 提示] 請輸入你想查詢的關鍵字或主題。範例: python matrix_ai_oracle.py '漏洞'")
            return

        print(f"🔮 [Oracle 正在解析] 正在智庫中全域搜尋與 '{keyword}' 相關的戰略情報...\n")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        results = []

        # 1. 搜尋一般情報智庫 (intel_vault)
        try:
            cursor.execute("SELECT title, link, 'General Intel' FROM intel_vault")
            for row in cursor.fetchall():
                results.append((row[0], row[1], row[2]))
        except Exception:
            pass

        # 2. 搜尋 OSINT 威脅情資 (osint_vault)
        try:
            cursor.execute("SELECT title, source_url, 'OSINT Threat' FROM osint_vault")
            for row in cursor.fetchall():
                results.append((row[0], row[1], row[2]))
        except Exception:
            pass

        conn.close()

        if not results:
            print("[❌ 智庫回報] 目前資料庫中尚無任何情報記錄。")
            return

        # 進行模糊匹配篩選
        matched_items = []
        for title, link, category in results:
            # 計算相似度
            match_ratio = difflib.SequenceMatcher(None, keyword.lower(), title.lower()).ratio()
            if keyword.lower() in title.lower() or match_ratio > 0.2:
                matched_items.append((title, link, category, match_ratio))

        # 依匹配度排序
        matched_items.sort(key=lambda x: x[3], reverse=True)

        print(f"================================================")
        print(f"📊 智庫查詢結果：找到 {len(matched_items)} 筆相關情資")
        print(f"================================================\n")

        if not matched_items:
            print("💡 沒有找到完全符合的項目，建議嘗試更廣泛的關鍵字。")
            return

        for idx, (title, link, category, score) in enumerate(matched_items[:5], 1):
            print(f"[{idx}] 類別: {category} (關聯度: {score:.2f})")
            print(f"    標題: {title}")
            print(f"    通道: {link}")
            print("-" * 50)

if __name__ == "__main__":
    search_keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    oracle = MatrixAIOracle()
    oracle.query_intel(search_keyword)

