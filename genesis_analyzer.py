import os
import datetime

class GenesisAnalyzer:
    def __init__(self, target_file="genesis_core_eternity.py"):
        self.target_file = target_file

    def analyze_core(self):
        print(f"-> 🔍 [分析模組] 正在深度掃描核心檔案: {self.target_file}")
        
        if not os.path.exists(self.target_file):
            print(f"-> ❌ 找不到目標檔案: {self.target_file}")
            return None

        file_size = os.path.getsize(self.target_file)
        
        with open(self.target_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if line.strip() == "")
        code_lines = total_lines - blank_lines
        
        # 計算基因片段數量 (依據我們之前設定的 GENE START 標籤)
        gene_count = sum(1 for line in lines if "# === [GENE START:" in line)

        report = {
            "file_name": self.target_file,
            "file_size_bytes": file_size,
            "total_lines": total_lines,
            "code_lines": code_lines,
            "blank_lines": blank_lines,
            "gene_fragments": gene_count,
            "analyzed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self._print_report(report)
        return report

    def _print_report(self, report):
        print("\n" + "=" * 40)
        print("📊 [Genesis 核心基因庫分析報告]")
        print("=" * 40)
        print(f"• 檔案名稱: {report['file_name']}")
        print(f"• 檔案大小: {report['file_size_bytes']} bytes")
        print(f"• 總行數: {report['total_lines']} 行")
        print(f"• 程式碼行數: {report['code_lines']} 行")
        print(f"• 空白行數: {report['blank_lines']} 行")
        print(f"• 內含基因片段: {report['gene_fragments']} 個")
        print(f"• 分析時間: {report['analyzed_at']}")
        print("=" * 40 + "\n")

if __name__ == "__main__":
    analyzer = GenesisAnalyzer()
    analyzer.analyze_core()
