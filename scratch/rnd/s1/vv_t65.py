import json
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
rows={r["fold"]:r for r in d["per_fold"]}
doc=open("docs/RND_S1_SEED_ROBUSTNESS.md",encoding="utf-8").read().splitlines()
def num(s):
    s=s.strip().replace("\u00a0","")
    return float(s.replace(",","."))
bad=[]; ncek=0
for ln in doc:
    if not ln.startswith("| F-"): continue
    c=[x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c)!=12: continue          # hanya baris tabel 6.5 (12 kolom)
    f=c[0]
    if f not in rows: continue
    r=rows[f]
    pairs=[("h",num(c[1]),float(r["h_terpilih"])),
           ("laju",num(c[2]),round(r["laju_alarm_kalibrasi"],6)),
           ("tp",num(c[4]),float(r["rows"]["tp"])),
           ("fp",num(c[5]),float(r["rows"]["fp"])),
           ("prec",num(c[6]),round(r["rows"]["precision"],4)),
           ("rec",num(c[7]),round(r["rows"]["recall"],4)),
           ("fark",num(c[8]),r["far24_kalender"]),
           ("farb",num(c[9]),r["far24_baris"]),
           ("lead",num(c[10]),float(r["lead"]["lead_median_min"])),
           ("dip",num(c[11]),float(r["lead"]["n_diperingatkan"]))]
    for nm,a,b in pairs:
        ncek+=1
        if abs(a-b)>5e-4: bad.append((f,nm,a,b))
print(f"sel tabel 6.5 diperiksa: {ncek}, tidak cocok: {len(bad)}")
for x in bad: print("  BEDA",x)
print("lolos anggaran di dokumen:", sum(1 for ln in doc if ln.startswith("| F-") and ln.count("|")==13 and "| ya |" in ln), "dari 9")
