"""Ulangi hitungan remark yang memuat durasi pada ddr_downtime_records.jsonl."""
import json, re, os
p = "/mnt/d/Capstone 1(v2)/scratch/rnd/s4/ddr_downtime_records.jsonl"
rx = re.compile(r"(\d+[.,]?\d*)\s*(hrs?|hours?|h|min|minutes?)", re.I)
n = 0
n_dur = 0
contoh = []
kolom = set()
for line in open(p, encoding="utf-8"):
    r = json.loads(line)
    n += 1
    kolom.add(tuple(sorted(r.keys())))
    rem = r.get("remark") or ""
    if rx.search(rem):
        n_dur += 1
        if len(contoh) < 5:
            contoh.append(rem[:120])
print("record:", n, "| dengan durasi di remark:", n_dur)
print("skema kunci unik:", len(kolom), list(kolom)[0])
for c in contoh:
    print("  contoh:", c)
