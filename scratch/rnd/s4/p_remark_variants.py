"""Rekonsiliasi hitungan remark durasi (beberapa varian regex) + distribusi equipment_repaired."""
import json, re, collections
p = "/mnt/d/Capstone 1(v2)/scratch/rnd/s4/ddr_downtime_records.jsonl"
rows = [json.loads(l) for l in open(p, encoding="utf-8")]
varian = {
    "A_jam_dan_menit": re.compile(r"(\d+[.,]?\d*)\s*(hrs?|hours?|h|min|minutes?)", re.I),
    "B_tanpa_minutes": re.compile(r"(\d+[.,]?\d*)\s*(hrs?|hours?|h|min)", re.I),
    "C_hanya_jam": re.compile(r"(\d+[.,]?\d*)\s*(hrs?|hours?)", re.I),
    "D_hanya_jam_kata_utuh": re.compile(r"(\d+[.,]?\d*)\s*\b(hours?|hrs?)\b", re.I),
}
for nama, rx in varian.items():
    hit = [r for r in rows if rx.search(r.get("remark") or "")]
    print(f"{nama}: {len(hit)} record")
print()
er = collections.Counter((r.get("equipment_repaired") or "").strip() for r in rows)
print("equipment_repaired nilai unik:", len(er))
for k, v in er.most_common(10):
    print(f"  {k!r}: {v}")
dt = collections.Counter(r.get("downtime_min") for r in rows)
print("downtime_min nilai unik:", len(dt), dict(list(dt.items())[:5]))
print("n_kolom distribusi:", collections.Counter(r.get("n_kolom") for r in rows))
