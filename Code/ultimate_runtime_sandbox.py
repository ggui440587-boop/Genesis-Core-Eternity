
import sys
def run_dynamic_workload():
    metric = sum([i * 2 for i in range(10)])
    print(f"動態沙盒計算成功，特徵檢核碼: {metric}")
    return metric

if __name__ == '__main__':
    run_dynamic_workload()
