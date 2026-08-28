import os
import random
import importlib.util
import sys
from pathlib import Path

class PrecisionEngine:
    """左側產線：獨立的精準育種與型態驗證"""
    def __init__(self, target_dir: str):
        self.dir = Path(target_dir)

    def breed(self, script_a: str, script_b: str, func_name: str, test_input):
        path_a, path_b = self.dir / script_a, self.dir / script_b
        if not path_a.exists() or not path_b.exists():
            return None, "[精準] 來源檔案不存在"

        try:
            spec_a = importlib.util.spec_from_file_location("p_a", str(path_a))
            mod_a = importlib.util.module_from_spec(spec_a)
            spec_a.loader.exec_module(mod_a)

            spec_b = importlib.util.spec_from_file_location("p_b", str(path_b))
            mod_b = importlib.util.module_from_spec(spec_b)
            spec_b.loader.exec_module(mod_b)

            if not hasattr(mod_a, func_name) or not hasattr(mod_b, func_name):
                return None, "[精準] 介面特徵不吻合，基因排斥"

            res_a = getattr(mod_a, func_name)(test_input)
            final_res = getattr(mod_b, func_name)(res_a)
            return final_res, "[精準] 育種與驗證成功"
        except Exception as e:
            return None, f"[精準] 執行崩潰已被隔離: {str(e)}"

class WildMutationEngine:
    """右側產線：獨立的野生盲撞與自然淘汰"""
    def __init__(self, target_dir: str):
        self.dir = Path(target_dir)

    def mutate(self):
        scripts = list(self.dir.glob("*.py"))
        # 排除自己以免撞到 main.py
        scripts = [s for s in scripts if s.name != "main.py"]
        
        if len(scripts) < 2:
            return "[野生] 樣本不足，無法碰撞"

        p_a, p_b = random.sample(scripts, 2)
        print(f"[野生] 正在隨機盲撞：{p_a.name} x {p_b.name}")
        
        # 透過管線讓 A 的輸出成為 B 的輸入
        exit_code = os.system(f"echo 'hello chaos' | python3 {p_a} | python3 {p_b}")
        
        if exit_code == 0:
            return f"[野生] 盲撞成功：{p_a.name} x {p_b.name}"
        else:
            return f"[野生] 盲撞崩潰（已自然淘汰）"

if __name__ == "__main__":
    workspace = "./"
    
    print("=== 1. 測試左側：精準育種產線 ===")
    precision_lab = PrecisionEngine(workspace)
    result, msg = precision_lab.breed("script_a.py", "script_b.py", "process", "hello genesis")
    print(msg)
    print(f"最終產物 -> {result}\n")
    
    print("=== 2. 測試右側：野生突變產線 ===")
    wild_lab = WildMutationEngine(workspace)
    wild_msg = wild_lab.mutate()
    print(wild_msg)
