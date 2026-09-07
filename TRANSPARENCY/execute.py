import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python runner.py <script.py> <times>")
    sys.exit(1)

script, times = sys.argv[1], int(sys.argv[2])

for i in range(times):
    print(f"\n--- Run {i+1} ---")
    subprocess.run(["python", script])