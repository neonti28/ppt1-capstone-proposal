import sys, json
sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
import rnd_hybrid_harness as H
import pandas as pd

DS = f"{H.DSD}/hyd_ki.csv.gz"
LOWO = f"{H.LOWOD}/lowo_hyd_ki.json"
df = H.muat_dataset(DS)
well_df = H.pecah_well(df)
folds = H.muat_fold(LOWO)
rec = H.jalankan_h1(seed=42, well_df=well_df, folds=folds)
r = H.ringkas_records(rec, "H1_stat_dan_rule")
print("jalankan_h1 H1:", {k: r[k] for k in ("fp_total", "tp_total", "precision_median", "recall_median")})
rr = H.ringkas_records(rec, "rule_kanal")
print("jalankan_h1 rule:", {k: rr[k] for k in ("fp_total", "tp_total")})
for x in rec:
    if x["model"] == "H1_stat_dan_rule":
        print(" fold", x["fold"], "fp", x["rows"]["fp"], "tp", x["rows"]["tp"], "h", x["h_terpilih"])

# manual same fold, explicit args
f = folds[0]
w = f["test_well"]
d = well_df[w]
sig = H.detektor_stat_rule(w, d["ts_bin"].to_numpy(int), f["train_wells"][0],
                           well_df[f["train_wells"][0]]["ts_bin"].to_numpy(int), chan="SPPA")
y = d["y_hyd"].to_numpy(int)
ev = H.evaluasi_fold(y, sig["h1"], d["ts_bin"].to_numpy(int))
print("manual fold", w, "fp", ev["rows"]["fp"], "tp", ev["rows"]["tp"], "h", sig["h"])
rule = H.gerbang_rule(w, d["ts_bin"].to_numpy(int))
evr = H.evaluasi_fold(y, rule, d["ts_bin"].to_numpy(int))
print("manual rule fold", w, "fp", evr["rows"]["fp"], "tp", evr["rows"]["tp"])
print("sha of lib:", __import__("hashlib").sha256(open("/mnt/d/Capstone 1(v2)/code/rnd_hybrid_harness.py","rb").read()).hexdigest()[:16])
print("mtime harness:", pd.Timestamp(__import__("os").path.getmtime("/mnt/d/Capstone 1(v2)/code/rnd_hybrid_harness.py"), unit="s", tz="UTC"))
print("mtime dataset:", pd.Timestamp(__import__("os").path.getmtime(DS), unit="s", tz="UTC"))
