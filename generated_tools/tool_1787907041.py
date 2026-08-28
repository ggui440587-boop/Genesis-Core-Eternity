import sys, os, datetime, math
print(f"[SYSTEM TELEMETRY] Time: {datetime.datetime.now()} | Platform: {sys.platform}")
print(f"[MATH STATS] Pi: {math.pi:.6f} | E: {math.e:.6f} | Calc: {sum(i**2 for i in range(100))}")
