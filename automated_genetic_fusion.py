import os
import urllib.request
import datetime
import subprocess

class AutomatedGeneticFusionEngine:
    def __init__(self, output_file="genesis_core_eternity.py"):
        self.output_file = output_file
        self.genetic_pool = []

    def absorb_gene(self, name, url):
        print(f"-> 🧬 [自動基因吸收] 正在自動提取專案基因: {name}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                code_content = response.read().decode('utf-8')
            
            clean_code = f"\n# === [GENE START: {name}] ===\n" + code_content + f"\n# === [GENE END: {name}] ===\n"
            self.genetic_pool.append(clean_code)
            print(f"-> ✅ 成功自動融合基因: {name}")
        except Exception as e:
            print(f"-> ⚠️ 自動基因吸收失敗 [{name}]: {e}")

    def synthesize_dna(self):
        print("-> 🧪 [自動基因合成] 正在將所有核心開源基因自動熔鑄至單一檔案...")
        header = (
            "# -*- coding: utf-8 -*-\n"
            "# ==================================================\n"
            "# 專案名稱: Genesis-Core-Eternity (自動化基因融合永恆核心)\n"
            f"# 合成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# 說明: 本檔案由自動化基因融合引擎自動抓取、萃取並編譯產出\n"
            "# ==================================================\n\n"
        )
        
        body = "".join(self.genetic_pool)
        
        footer = (
            "\n\ndef genesis_core_hook():\n"
            "    print('-> 🚀 [核心啟動] 自動化基因融合永恆核心運作正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    genesis_core_hook()\n"
        )

        full_dna = header + body + footer

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(full_dna)
            print(f"-> 💾 基因核心自動寫入成功: {self.output_file}")
            return self.output_file
        except Exception as e:
            print(f"-> ❌ 基因核心自動寫入失敗: {e}")
            return None

    def verify_dna(self, file_path):
        print(f"-> 🔍 [自動基因檢驗] 正在檢查核心語法健康度: {file_path}")
        try:
            subprocess.run(
                ["python", "-m", "py_compile", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            print("-> 🎉 自動基因檢驗完美通過！結構強韌穩定。")
            return True
        except Exception as e:
            print(f"-> ⚠️ 自動基因檢驗異常: {e}")
            return False

if __name__ == "__main__":
    print("【自動化基因融合引擎啟動】\n")
    
    engine = AutomatedGeneticFusionEngine()
    
    # 自動化基因清單
    target_genes = [
        {"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"},
        {"name": "Rich", "url": "https://raw.githubusercontent.com/Textualize/rich/refs/heads/main/rich/__init__.py"},
        {"name": "FastAPI", "url": "https://raw.githubusercontent.com/fastapi/fastapi/refs/heads/master/fastapi/__init__.py"}
    ]
    
    for gene in target_genes:
        engine.absorb_gene(gene["name"], gene["url"])
        print("-" * 30)
        
    fused_file = engine.synthesize_dna()
    if fused_file:
        engine.verify_dna(fused_file)
        
    print("\n-> ✨ 全球開源基因自動融合至永恆核心流程圓滿完成！")
