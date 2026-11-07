import json, hashlib, subprocess, re
meta=json.load(open("scratch/rnd/s1/s1_meta.json"))
h=hashlib.sha256(open("code/rnd_hybrid_harness.py","rb").read()).hexdigest()
print("meta tanggal:", meta["tanggal"], "| elapsed_s:", meta["elapsed_s"], "| perintah:", meta["perintah"])
print("harness sha di meta == sha file sekarang:", meta["harness_sha256"]==h, "|", h[:16])
print("r8 sha di meta:", meta["r8_sha256"][:16])
print("dataset sha:", meta["dataset_sha256"][:16], "shape:", meta["dataset_shape"], "n_fold:", meta["n_fold"])
d=json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
f42={r["fold"]:r for r in d["per_seed"]["42"]["folds"] if r["model"]=="H1_stat_dan_rule"}
txt=open("docs/RND_S1_SEED_ROBUSTNESS.md",encoding="utf-8").read()
blk=txt[txt.index("## 4."):txt.index("## 5.")]
def num(s): return float(s.strip().replace(",","."))
bad=0; n=0
for ln in blk.splitlines():
    if not ln.startswith("| F-"): continue
    c=[x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c)<6: continue
    f=c[0]; r=f42[f]; n+=1
    for idx,key in ((1,"fp"),(3,"tp")):
        pass
    # tabel 1 di bagian 4 punya 9 kolom: Fold,FP R8,FP S1,Delta,TP R8,TP S1,Delta,h R8,h S1
    if len(c)==9:
        vals=[num(c[1]),num(c[2]),num(c[4]),num(c[5]),num(c[7]),num(c[8])]
        exp=[r["rows"]["fp"]]*2+[r["rows"]["tp"]]*2+[float(r["h_terpilih"])]*2
        if any(abs(a-b)>1e-6 for a,b in zip(vals,exp)): bad+=1; print("  BEDA",f,c)
print(f"\ntabel bagian 4: {n} baris fold diperiksa, beda: {bad}")
print("em-dash di dokumen:", txt.count("\u2014"))
print("ada ringkasan lima baris:", "### 8.3 Ringkasan lima baris" in txt, "| ada daftar belum terverifikasi:", "### 8.4" in txt)
tail=txt[txt.index("### 8.3"):]
print("jumlah item ringkasan:", len(re.findall(r"^\d\. ", tail, flags=re.M)))
