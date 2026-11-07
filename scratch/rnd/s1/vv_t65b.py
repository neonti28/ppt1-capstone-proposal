import json
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
rows={r["fold"]:r for r in d["per_fold"]}
txt=open("docs/RND_S1_SEED_ROBUSTNESS.md",encoding="utf-8").read()
blk=txt[txt.index("### 6.5"):txt.index("## 7.")]
def num(s): return float(s.strip().replace(",","."))
bad=[]; ncek=0; nyaris=0
for ln in blk.splitlines():
    if not ln.startswith("| F-"): continue
    c=[x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c)!=12: continue
    r=rows[c[0]]
    pairs=[("h",num(c[1]),float(r["h_terpilih"])),("laju",num(c[2]),round(r["laju_alarm_kalibrasi"],6)),
           ("tp",num(c[4]),float(r["rows"]["tp"])),("fp",num(c[5]),float(r["rows"]["fp"])),
           ("prec",num(c[6]),round(r["rows"]["precision"],4)),("rec",num(c[7]),round(r["rows"]["recall"],4)),
           ("fark",num(c[8]),r["far24_kalender"]),("farb",num(c[9]),r["far24_baris"]),
           ("lead",num(c[10]),float(r["lead"]["lead_median_min"])),("dip",num(c[11]),float(r["lead"]["n_diperingatkan"]))]
    nyaris+=1
    for nm,a,b in pairs:
        ncek+=1
        if abs(a-b)>5e-4: bad.append((c[0],nm,a,b))
print(f"baris 6.5: {nyaris}, sel diperiksa: {ncek}, tidak cocok: {len(bad)}")
for x in bad: print("  BEDA",x)
print("kolom 'ya':", sum(1 for ln in blk.splitlines() if ln.startswith("| F-") and "| ya |" in ln), "dari", nyaris)
