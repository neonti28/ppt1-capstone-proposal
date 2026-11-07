import json
import re

S = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s3/s3c_ringkas.json"))
h = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s3/s3b_hybrid.json"))
print("CAKUPAN_MIN / FAR_MAKS / RECALL_MIN di harness:")
src = open("/mnt/d/Capstone 1(v2)/code/rnd_hybrid_harness.py").read()
for k in ("CAKUPAN_MIN", "FAR_MAKS", "RECALL_MIN", "ALPHA_BUDGET", "W_ALARM", "WIN_Z"):
    m = re.search(rf"^{k}\s*=\s*(.+)$", src, re.M)
    print(" ", k, "=", m.group(1) if m else "TIDAK ADA")
print("\nfar per fold (H5) dari records:")
for r in h["records"]:
    if r["model"] == "H5_stat_dan_rule":
        f = r["far"]
        print(f"{r['fold'][:26]:28s} berdata={f['menit_berdata']:5d} rentang={f['rentang_menit']:8.0f} "
              f"cakupan={f['cakupan_menit']} pos={f['menit_pos']:5d} neg={f['menit_neg']:5d} "
              f"jam_ops={f['jam_operasi']:8.2f} alarm_neg={f['menit_alarm_neg']:4d} far24={f['far24_kalender']}")
