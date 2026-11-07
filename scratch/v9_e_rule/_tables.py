import json

OUT = "/mnt/d/Capstone 1/scratch/v9_e_rule"
r1 = json.load(open(f"{OUT}/v9_e_RULE_01_status_results.json"))
r2 = json.load(open(f"{OUT}/v9_e_RULE_02_stuck_onset_results.json"))
r3 = json.load(open(f"{OUT}/v9_e_RULE_03_bitwear_toolwear_results.json"))
r4 = json.load(open(f"{OUT}/v9_e_RULE_04_hyd_k2_results.json"))


def f4(x):
    return "-" if x is None else (f"{x:.4f}" if isinstance(x, float) else str(x))


for cls, d in r1["classes"].items():
    print(f"\n### {cls}")
    print("| fold | well | n | pos | prev | UP | pers | persVP | rule | FP | P | R | FAR24 | hyb FP hybP | can rand |")
    for f in d["folds"]:
        p = f["persistence"]
        rd = f["rule_display_t0minus1"]
        hb = f["hybrid_rule_and_persistence"]
        extra = ""
        if "rule_E1_2of3" in f:
            e = f["rule_E1_2of3"]
            extra = f"| E1 {f4(e['auprc'])} FP{e['fp']} P{f4(e['precision'])} |"
        print(f"| {f['fold']} | {f['test_well']} | {f['n']} | {f['pos']} | {f4(f['prev'])} | "
              f"{'Y' if f['underpowered'] else '.'} | {f4(p['auprc'])} | {f4(p['auprc_validprev'])} | "
              f"{f4(rd['auprc'])} | {rd['fp']} | {f4(rd['precision'])} | {f4(rd['recall'])} | {f4(rd['far_24h'])} | "
              f"{hb['fp']} {f4(hb['precision'])} | {f4(f['canary_depth']['auprc'])} {f4(f['prevalence_random']['auprc_emp'])} | {extra}")

print("\n### stuck_k2")
print("| fold | well | n | pos | prev | onsets | persH auprc | B1 | TLead med | persE auprc | B1 | E1 auprc | B1 | FP | canary |")
for f in r2["folds"]:
    ph, pe, e1 = f["persistence_horizon"], f["persistence_event"], f["rule_E1_2of3"]
    print(f"| {f['fold']} | {f['test_well']} | {f['n']} | {f['pos']} | {f4(f['prev'])} | {f['n_onsets']} | "
          f"{f4(ph['auprc'])} | {f4(ph['onset']['b1'])} | {f4(ph['onset']['tlead_min']['median'])} | "
          f"{f4(pe['auprc'])} | {f4(pe['onset']['b1'])} | {f4(e1['auprc'])} | {f4(e1['onset']['b1'])} | {e1['fp']} | "
          f"{f4(f['canary_depth']['auprc'])} |")

print("\n### bit_wear K-1")
for f in r3["bitwear_k1"]["folds"]:
    p = f["persistence"]
    print(f"| {f['test_well']} | n={f['n']} pos={f['pos']} prev={f4(f['prev'])} UP={'Y' if f['underpowered'] else '.'} "
          f"pers={f4(p['auprc'])} (n={p['n_persistence']}) can={f4(f['canary_depth']['auprc'])} "
          f"rand={f4(f['prevalence_random']['auprc_emp'])} xchk={f['crosscheck_v6']} |")

print("\n### tool_wear K-ii")
for f in r3["toolwear_kii"]["folds"]:
    print(f"| {f['test_tool']} | n={f['n']} pos={f['pos']} can3rms={f4(f['canary_3rms']['auprc'])} "
          f"prev={f4(f['prev'])} persDiag={f4(f['persistence_diagnostic']['auprc'])} |")

print("\n### hyd K-ii")
print(json.dumps(r4["test"], indent=1)[:1500])
