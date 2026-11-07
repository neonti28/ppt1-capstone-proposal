"""Probe: tampilkan struktur tabel downtime pada satu DDR HTML."""
import re, os, html
ROOT = "/mnt/d/Capstone 1(v2)"
P = os.path.join(ROOT, "data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version/15_9_F_10_2009_04_12.html")
txt = open(P, encoding="utf-8", errors="replace").read()
tables = re.findall(r"<table[^>]*>.*?</table>", txt, flags=re.S)
print("n_tabel:", len(tables))
for i, t in enumerate(tables):
    if "Operation Downtime" in t:
        print("=== tabel", i, "panjang", len(t))
        heads = re.findall(r"<th[^>]*>(.*?)</th>", t, flags=re.S)
        print("HEADER:", [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in heads])
        rows = re.findall(r"<tr>(.*?)</tr>", t, flags=re.S)
        print("n_tr:", len(rows))
        for r in rows[:4]:
            cells = re.findall(r"<td[^>]*>(.*?)</td>|<td[^>]*/>", r, flags=re.S)
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells]
            print("ROW:", cells)
        break
else:
    print("tidak ada tabel downtime di file ini")
