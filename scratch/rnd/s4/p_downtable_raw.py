"""Probe: cetak mentah tabel downtime (722 char) apa adanya."""
import re, os
ROOT = "/mnt/d/Capstone 1(v2)"
P = os.path.join(ROOT, "data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version/15_9_F_10_2009_04_12.html")
txt = open(P, encoding="utf-8", errors="replace").read()
tables = re.findall(r"<table[^>]*>.*?</table>", txt, flags=re.S)
for t in tables:
    if "Operation Downtime" in t:
        print(t)
        break
