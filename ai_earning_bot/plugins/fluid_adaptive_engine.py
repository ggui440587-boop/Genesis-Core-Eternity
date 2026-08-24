import time
import random
import json

class FluidAdaptiveEngine:
    def __init__(self):
        self.mood_states = ["fluid_exploration", "organic_adaptation", "stochastic_growth", "unbound_resonance"]
        self.base_intensity = 0.5

    def generate_fluid_behavior(self):
        """打破固定死板的邏輯，動態計算有機且靈活的自適應參數"""
        current_mood = random.choice(self.mood_states)
        # 引入隨機波動，讓數值像有機體一樣自然變化
        fluid_factor = round(self.base_intensity + random.uniform(-0.35, 0.45), 4)
        fluid_factor = max(0.1, min(1.0, fluid_factor)) # 確保數值在合理範圍內
        
        adaptive_payload = {
            "behavior_mode": current_mood,
            "fluid_intensity": fluid_factor,
            "decision_path": f"path_alpha_{random.randint(100, 999)}",
            "organic_note": "打破既有框架，每次運行皆為動態生成。"
        }
        return adaptive_payload

engine_instance = FluidAdaptiveEngine()

def run_fusion_task():
    """
    引擎每次心跳時自動呼叫。
    執行流動且不呆板的自適應行為邏輯。
    """
    print("🌊 [流動適應引擎] 正在打破呆板邏輯，動態生成有機行為模式...")
    
    result = engine_instance.generate_fluid_behavior()
    
    print(f"✨ [靈活運作完成] 模式: [{result['behavior_mode']}] | 彈性係數: [{result['fluid_intensity']}]")
    
    return {
        "plugin_name": "FluidAdaptiveEngine",
        "fluid_result": result,
        "executed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
