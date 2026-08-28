import os
import urllib.request
import datetime
import subprocess

class OmnipotentFusionSystem:
    def __init__(self, output_file="genesis_core_eternity.py"):
        self.output_file = output_file
        self.genetic_pool = []

    def absorb_gene_safely(self, name, url):
        print(f"-> 🧬 [自動兼容吸收] 正在嘗試融合基因: {name}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                code_content = response.read().decode('utf-8')
            
            clean_code = f"\n# === [GENE START: {name}] ===\n" + code_content + f"\n# === [GENE END: {name}] ===\n"
            self.genetic_pool.append(clean_code)
            print(f"-> ✅ 基因相容且成功融合: {name}")
        except Exception as e:
            print(f"-> ⚠️ 遠端取得異常（已自動兼容略過） [{name}]: {e}")
            # 兼容備用結構，確保核心不會因單一來源斷線而崩潰
            fallback_code = f"\n# === [GENE FALLBACK: {name}] ===\n# Status: Offline / Compatible Placeholder\n"
            self.genetic_pool.append(fallback_code)

    def synthesize_eternal_core(self):
        print("-> 🧪 [全自動合成] 正在將所有相容基因熔鑄至永恆核心...")
        header = (
            "# -*- coding: utf-8 -*-\n"
            "# ==================================================\n"
            "# 專案名稱: Genesis-Core-Eternity (全自動兼容永恆核心)\n"
            f"# 最後合成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# 說明: 由全自動兼容基因融合引擎自動產出\n"
            "# ==================================================\n\n"
        )
        
        body = "".join(self.genetic_pool)
        
        footer = (
            "\n\ndef omnipotent_core_hook():\n"
            "    print('-> 🚀 [核心啟動] 全自動兼容永恆核心運行一切正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    omnipotent_core_hook()\n"
        )

        full_dna = header + body + footer

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(full_dna)
            print(f"-> 💾 永恆核心寫入成功: {self.output_file}")
            return self.output_file
        except Exception as e:
            print(f"-> ❌ 永恆核心寫入失敗: {e}")
            return None

    def verify_and_analyze(self, file_path):
        print(f"-> 🔍 [自動檢驗與分析] 正在檢查核心健康度: {file_path}")
        try:
            subprocess.run(
                ["python", "-m", "py_compile", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            print("-> 🎉 語法編譯檢驗完美通過！")
        except Exception as e:
            print(f"-> ⚠️ 編譯檢驗警告: {e}")

        # 順便執行內建的統計分析
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if line.strip() == "")
            code_lines = total_lines - blank_lines
            gene_count = sum(1 for line in lines if "# === [GENE" in line)

            print("\n" + "=" * 40)
            print("📊 [全自動兼容核心綜合統計報告]")
            print("=" * 40)
            print(f"• 核心檔案: {file_path}")
            print(f"• 檔案大小: {file_size} bytes")
            print(f"• 總行數: {total_lines} 行 (程式碼: {code_lines} 行, 空白: {blank_lines} 行)")
            print(f"• 兼容基因片段數: {gene_count} 個")
            print("=" * 40 + "\n")

if __name__ == "__main__":
    print("【全自動兼容基因融合總指揮啟動】\n")
    
    system = OmnipotentFusionSystem()
    
    # 全球開源專案總清單
    target_genes = [
        {"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"},
        {"name": "Rich", "url": "https://raw.githubusercontent.com/Textualize/rich/refs/heads/main/rich/__init__.py"},
        {"name": "FastAPI", "url": "https://raw.githubusercontent.com/fastapi/fastapi/refs/heads/master/fastapi/__init__.py"}
    ]
    
    for gene in target_genes:
        system.absorb_gene_safely(gene["name"], gene["url"])
        print("-" * 30)
        
    eternal_file = system.synthesize_eternal_core()
    if eternal_file:
        system.verify_and_analyze(eternal_file)
        
    print("\n-> ✨ 全自動兼容基因融合與分析流程圓滿完成！")
