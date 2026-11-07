# Falsifier: setiap angka kunci di docs/V10_E_STAT_BAB.md harus ada di JSON sumber.
import json, os, re
B="/mnt/d/Capstone 1(v2)"
doc=open(B+"/docs/V10_E_STAT_BAB.md",encoding="utf-8").read()
doc_flat=" ".join(doc.split())   # normalisasi whitespace (baris wrap markdown)
J={f:json.load(open(f"{B}/scratch/v9_e_stat/{f}")) for f in
   ["v9_e_stat_01_hyd_ki_RESULTS.json","v9_e_stat_02_stuck_e2_RESULTS.json",
    "v9_e_stat_03_tool_wear_RESULTS.json","v9_e_stat_04_fisher_pearson_RESULTS.json"]}
checks=[]
def chk(name, cond): checks.append((name,bool(cond)))

# hyd K-i
h1=J["v9_e_stat_01_hyd_ki_RESULTS.json"]; s=h1["summary"]
chk("hyd auprc_range 0.4245-0.8426", s["auprc_range_layak"]==[0.4245,0.8426])
chk("hyd lift_range 2.388-6.102", s["lift_range_layak"]==[2.388,6.102])
chk("hyd lift>1 9/9", s["lift_gt1_folds"]==9)
chk("hyd dB>0 9/9", s["dB_pos_folds"]==9)
chk("hyd crosscheck 0/52509", h1["label_crosscheck"]["total_y_mismatch"]==0 and h1["label_crosscheck"]["total_rows"]==52509)
chk("doc hyd crosscheck 0/52.509", "0/52.509" in doc and "0 mismatch / 52.509" in doc)
chk("doc hyd lift 2,39-6,10", "2,39–6,10" in doc)
chk("doc hyd RF 7/7", "7/7 fold" in doc)

# stuck E2
h2=J["v9_e_stat_02_stuck_e2_RESULTS.json"]; s2=h2["summary"]
chk("stuck lift_range 1.057-1.797", s2["lift_range_layak"]==[1.057,1.797])
chk("stuck ci memuat prev 4/4", s2["ci95_contains_prev_folds"]==4)
chk("stuck onset_runs 281", s2["onset_runs_total"]==281)
chk("doc stuck lift 1,06-1,80", "1,057–1,797" in doc and "1,06–1,80" in doc)
thrs=[f["thr_q95_train"] for f in h2["folds"]]
chk("stuck thr 4 nilai", thrs==[2.464889,2.821882,2.762111,2.51442])
chk("doc stuck thr 2,4649..", "2,4649 / 2,8219 / 2,7621 / 2,5144" in doc_flat)
onsets=[f["n_onsets_from_runs"] for f in h2["folds"]]
chk("stuck onsets 93/61/55/72", onsets==[93,61,55,72])

# tool_wear
h3=J["v9_e_stat_03_tool_wear_RESULTS.json"]; s3=h3["summary"]
chk("tw cp_sig 8/8 p05", s3["cp_sig_p05"]==8)
chk("tw cp_sig 8/8 p002", s3["cp_sig_p002"]==8)
chk("tw calib 4/4", s3["calibration_det_R02"]=="4/4")
chk("tw auprc 0.5888 lift 1.151", s3["auprc_engine"]==0.5888 and s3["lift"]==1.151)
chk("tw prev identity 0.5117", h3["part_D_ranking_auprc"]["prev_identity_run"]==0.5117)
chk("tw precision cp 0.50", h3["part_A_change_point"]["run_level_sig_p05_v8"]["precision"]==0.5)
# FAR-calibrated: FP 1/3/1/3, TLead 25/36/24/20
op=[r for r in h3["part_C_operating_far_calibrated"] if r["target_fp_per_min"]==1.0]
chk("tw FARcal FP 1/3/1/3", [r["fp_R01"] for r in op]==[1,3,1,3])
chk("tw FARcal TLead 25/36/24/20", [r["TLead_s"] for r in op]==[25.0,36.0,24.0,20.0])
chk("doc tw FARcal table", "1 / 3 / 1 / 3" in doc and "25 / 36 / 24 / 20" in doc)

# fisher
h4=J["v9_e_stat_04_fisher_pearson_RESULTS.json"]
chk("fisher episodes 124=39/85", h4["label_Kii"]["n_episodes"]==124 and h4["label_Kii"]["n_kick"]==39 and h4["label_Kii"]["n_loss"]==85)
chk("fisher prev 0.003701", h4["engine_fisher_pearson_variant"]["prev"]==0.003701)
chk("fisher auprc 0.022", h4["engine_fisher_pearson_variant"]["auprc"]==0.022)
o=h4["engine_fisher_pearson_variant"]["op_q95"]
chk("fisher P=R=0 TP=0 FP=177", o["precision"]==0.0 and o["recall"]==0.0 and o["tp"]==0 and o["fp"]==177)
chk("doc fisher P=R=0", "0,000 / 0,000" in doc and "TP=0, FP=177" in doc)
chk("doc fisher literal tidak bisa", "TIDAK BISA DIJALANKAN" in doc)

# struktur bab
for sec in ["## 5.0","## 5.1","## 5.2","## 5.3","## 5.4","## 5.5","## 5.6"]:
    chk("ada seksi "+sec, sec in doc)
chk("baris Riset pendahuluan", "Riset pendahuluan:" in doc)
chk("skill scientific-critical-thinking", "scientific-critical-thinking" in doc)
chk("skill verification-mandatory", "verification-mandatory" in doc)
chk("skill statistical-analysis", "statistical-analysis" in doc)
chk("sequentialthinking 4 pikiran", "4 pikiran, 4/4 sukses" in doc)
chk("kosakata 7/11/27", "7/11/27" in doc and "27 head" in doc)

ok=sum(1 for _,c in checks if c)
print(f"LULUS {ok}/{len(checks)}")
for n,c in checks:
    if not c: print("  GAGAL:",n)
print("SEMUA LULUS" if ok==len(checks) else "ADA YANG GAGAL")
