# ==============================================================
# Pipeline Controller - 讀書與行動全流程串聯主控模組
# ==============================================================

from study_module import StudyModule
from knowledge_executor import KnowledgeExecutor

def main():
    print("=" * 60)
    print(" 🚀 啟動完整生態系：從「讀書」到「動起來」的全自動化流程")
    print("=" * 60)

    # 1. 執行讀書模組：吸收新知識
    study = StudyModule()
    study.read_and_absorb(
        topic="Python 模組化整合實作", 
        content="理解了透過 import 將獨立的讀書與動作模組串聯起來的完整架構。"
    )

    print("-" * 60)

    # 2. 執行知識轉化與行動模組：讓知識付諸實行
    executor = KnowledgeExecutor()
    executor.execute_latest_knowledge()

    print("=" * 60)
    print(" ✨ 全流程自動化執行完畢！")
    print("=" * 60)

if __name__ == "__main__":
    main()

