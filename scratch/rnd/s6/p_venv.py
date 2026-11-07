import glob
import os
import subprocess
import sys

print("python sekarang:", sys.version.split()[0], sys.executable)
for v in sorted(glob.glob("/home/neonti/.venv*") + glob.glob("/home/neonti/.venvs/*")):
    exe = os.path.join(v, "bin", "python3")
    if not os.path.exists(exe):
        continue
    r = subprocess.run([exe, "-c", "import pandas,numpy;print(pandas.__version__, numpy.__version__)"],
                       capture_output=True, text=True)
    print(f"{v}: rc={r.returncode} {r.stdout.strip()} {r.stderr.strip()[:100]}")
