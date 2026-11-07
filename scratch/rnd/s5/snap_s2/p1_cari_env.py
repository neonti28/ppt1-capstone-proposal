#!/usr/bin/env python3
"""Cek isi modul pada beberapa interpreter kandidat tanpa menyentuh data."""
import json
import subprocess
import sys

KANDIDAT = [
    "/home/neonti/.venvs/rnd_e3/bin/python3",
    "/home/neonti/.venvs/rnd_r3/bin/python3",
    "/home/neonti/.venv_audit/bin/python3",
    "/usr/bin/python3.14",
    "/home/neonti/.local/bin/python3.11",
]

SNIP = (
    "import json,sys\n"
    "o={'v':sys.version.split()[0],'m':{}}\n"
    "for m in ('numpy','pandas','scipy','sklearn','lightgbm'):\n"
    "    try:\n"
    "        mod=__import__(m); o['m'][m]=getattr(mod,'__version__','?')\n"
    "    except Exception as e:\n"
    "        o['m'][m]='MISSING'\n"
    "print(json.dumps(o))\n"
)

hasil = {}
for exe in KANDIDAT:
    try:
        r = subprocess.run([exe, "-c", SNIP], capture_output=True, text=True, timeout=120)
        hasil[exe] = r.stdout.strip() if r.returncode == 0 else f"ERR rc={r.returncode}: {r.stderr.strip()[:200]}"
    except Exception as e:
        hasil[exe] = f"GAGAL: {type(e).__name__}: {e}"
print(json.dumps(hasil, indent=1))
