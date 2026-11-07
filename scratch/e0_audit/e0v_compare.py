import json

W = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b/"
old = json.load(open(W + "e0_audit_results_baseline04.json"))
new = json.load(open(W + "e0_audit_results.json"))

diffs = []
same = []


def cmp(path, a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            cmp(f"{path}.{k}", a.get(k), b.get(k))
    else:
        if a == b:
            same.append(path)
        else:
            diffs.append((path, a, b))


cmp("root", old, new)
print("field identik:", len(same))
print("field beda  :", len(diffs))
for p, a, b in diffs[:25]:
    print("  BEDA", p, "lama=", a, "baru=", b)
print()
print("rule hash run1/run2 (baru):", {k: (v.get("rule_hash_run1"), v.get("rule_hash_run2"), v.get("rule_bit_identik")) for k, v in new["rule"].items()})
print("RF baru:", {k: new["determinisme_rf"].get(k) for k in ("hash1", "hash2", "skor_bit_identik", "max_abs_diff", "n_train", "n_test")})
print("leakage nol?", {k: v["n_feat_ts_max_ge_lab_ts"] for k, v in new["leakage"].items()})
out = {"n_field_identik": len(same), "n_field_beda": len(diffs),
       "beda": [{"path": p, "lama": a, "baru": b} for p, a, b in diffs],
       "rule_hash_baru": {k: [v.get("rule_hash_run1"), v.get("rule_hash_run2")] for k, v in new["rule"].items()},
       "rf_baru": {k: new["determinisme_rf"].get(k) for k in ("hash1", "hash2", "skor_bit_identik", "max_abs_diff")}}
json.dump(out, open(W + "e0v_rerun_compare.json", "w"), indent=1)
