import json, re
old=open("scratch/rnd/s1/bak/doc_0437.md",encoding="utf-8").read()
new=open("docs/RND_S1_SEED_ROBUSTNESS.md",encoding="utf-8").read()
num=lambda s: set(re.findall(r"\d+(?:[.,]\d+)?", s))
a,b=num(old),num(new)
print("angka hanya di dokumen lama:", sorted(a-b)[:20])
print("angka hanya di dokumen baru:", sorted(b-a)[:25])
# verifikasi tabel 6.5 terhadap artefak
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
rows={r["fold"]:r for r in d["per_fold"]}
print("\ncek tabel 6.5 (fold, h, laju, tp, fp, presisi, recall, fark, farb, lead, dip):")
ok=True
for f in sorted(rows):
    r=rows[f]
    exp=(int(r["h_terpilih"]) if float(r["h_terpilih"]).is_integer() else r["h_terpilih"],
         round(r["laju_alarm"],6), r["rows"]["tp"], r["rows"]["fp"],
         round(r["rows"]["precision"],4) if r["rows"]["precision"] is not None else None,
         round(r["rows"]["recall"],4) if r["rows"]["recall"] is not None else None,
         r["far24_kalender"], r["far24_baris"], r["lead"]["lead_median_min"], r["lead"]["n_diperingatkan"])
    # baris tabel di dokumen
    m=[ln for ln in new.splitlines() if ln.startswith(f"| {f} |") and ln.count("|")==13]
    print(f"  {f}: artefak={exp}")
print("\nlaju unik:", sorted({round(r['laju_alarm'],6) for r in d['per_fold']}))
print("h unik:", sorted({r['h_terpilih'] for r in d['per_fold']}))
print("\n=== 8.4 ===")
print(new[new.index("### 8.4"):][:2200])
