#!/usr/bin/env python3
import json
BASE = "/mnt/d/Capstone 1(v2)/scratch"
ec = json.load(open(f"{BASE}/v9_eval_c/v9_eval_c_RESULTS.json"))

def get(d, *path, default="<MISSING>"):
    for p in path:
        if isinstance(d, dict) and p in d:
            d = d[p]
        else:
            return default
    return d

def show(label, val):
    print(f"{label} = {val}")

print("### vib rule")
for k in ("C_rule_status",):
    v = ec.get(k, {})
    if "vib" in v:
        print(json.dumps(v["vib"], indent=1)[:1200])

print("\n### ssi rule/hybrid")
if "ssi" in ec.get("C_rule_status", {}):
    print(json.dumps(ec["C_rule_status"]["ssi"], indent=1)[:1500])

print("\n### shk rule")
if "shk" in ec.get("C_rule_status", {}):
    print(json.dumps(ec["C_rule_status"]["shk"], indent=1)[:1200])

print("\n### stuck K-i rule")
for key in ec.get("C_rule_status", {}):
    if "stuck" in key:
        print(key, json.dumps(ec["C_rule_status"][key], indent=1)[:900])

print("\n### hyd K-i rule")
for key in ec.get("C_rule_status", {}):
    if "hyd" in key:
        print(key, json.dumps(ec["C_rule_status"][key], indent=1)[:1200])

print("\n### C_onset stuck_k2")
print(json.dumps(ec.get("C_onset", {}), indent=1)[:2500])

print("\n### C_bitwear")
print(json.dumps(ec.get("C_bitwear", {}), indent=1)[:1500])

print("\n### C_toolwear")
print(json.dumps(ec.get("C_toolwear", {}), indent=1)[:2500])

print("\n### C_stat")
print(json.dumps(ec.get("C_stat", {}), indent=1)[:2500])

print("\n### C_ml vib/ssi/shk auprc disp")
for eng in ("vib", "ssi", "shk", "stuck_k2"):
    ml = ec.get("C_ml", {}).get(eng, {})
    rf = ml.get("rf", {})
    print(eng, "rf.auprc_disp =", rf.get("auprc_disp"))
