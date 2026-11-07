"""Tampilkan konteks 200 karakter di sekitar kemunculan 'price' pada berkas yang sama."""
import os, re
BASE = "/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data"
for sub, name in [("Daily Drilling Report - XML Version", "15_9_F_15_D_2013_11_12.xml"),
                  ("Daily Drilling Report - HTML Version", "15_9_F_15_D_2013_11_12.html")]:
    p = os.path.join(BASE, sub, name)
    txt = open(p, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"price", txt, re.I):
        s = max(0, m.start() - 200)
        e = min(len(txt), m.end() + 200)
        print("=" * 70)
        print(sub, "| posisi", m.start(), "| panjang berkas", len(txt))
        print(repr(txt[s:e]))
