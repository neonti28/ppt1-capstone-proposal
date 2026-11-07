import json

base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
base_j = json.load(open(f"{base}/e4_baseline.json"))
hyb = json.load(open(f"{base}/e4_hybrid.json"))
a1 = json.load(open(f"{base}/e4_a1.json"))

FAR_MAKS = 6.0
CAKUPAN_MIN = 0.50
RECALL_MIN = 0.50


def decompose(rows, name):
    n = len(rows)

    def cnt(field, thr, key=None):
        if key is None:
            return sum(1 for r in rows if (r.get(field) is not None and r[field] <= thr))
        return sum(1 for r in rows if (r.get(field) is not None and r[field] <= thr
                                       and (r["rows"]["recall"] or 0) >= RECALL_MIN))

    rec_ok = sum(1 for r in rows if (r["rows"]["recall"] or 0) >= RECALL_MIN)
    cak_ok = sum(1 for r in rows if ((r.get("cakupan") or {}).get("fraksi") or 0) >= CAKUPAN_MIN)

    def all3(field):
        return sum(1 for r in rows
                   if (r.get(field) is not None and r[field] <= FAR_MAKS)
                   and (r["rows"]["recall"] or 0) >= RECALL_MIN
                   and ((r.get("cakupan") or {}).get("fraksi") or 0) >= CAKUPAN_MIN)

    nol_alarm = sum(1 for r in rows if r["rows"]["fp"] == 0 and r["rows"]["tp"] == 0)
    return dict(n=n,
                far_ok_baris=cnt("far24_kalender", FAR_MAKS),
                far_ok_kejadian=cnt("far24_kalender_kejadian", FAR_MAKS),
                recall_ok=rec_ok, cakupan_ok=cak_ok,
                far_dan_recall_baris=cnt("far24_kalender", FAR_MAKS, "r"),
                far_dan_recall_kejadian=cnt("far24_kalender_kejadian", FAR_MAKS, "r"),
                ketiga_baris=all3("far24_kalender"),
                ketiga_kejadian=all3("far24_kalender_kejadian"),
                fold_tanpa_alarm=nol_alarm)


out = {}
for nm in ("persistence", "rule_t0m1", "hybrid_rule_persistence", "hybrid_proxy_E3"):
    rows = [r for r in base_j["folds"] if r.get("model") == nm]
    if rows:
        out[nm] = decompose(rows, nm)
for nm in ("H_and_hybrid_ML", "H_or_hybrid_ML"):
    rows = [r for r in hyb["folds"] if r.get("model") == nm]
    if rows:
        out[nm] = decompose(rows, nm)
for var in ("alpha_E2_lama", "alpha_anggaran"):
    rows = [r for r in a1["folds"] if r.get("varian") == var]
    if rows:
        out[f"A1_{var}"] = decompose(rows, var)

json.dump(out, open(f"{base}/e4_gate_decomp.json", "w"), indent=2)

print("%-26s %3s %8s %10s %9s %8s %8s %8s %8s %10s" % (
    "varian", "n", "FAR<=6 br", "FAR<=6 kej", "recall>=.5", "cakup>=.5",
    "3syarat br", "3syarat kj", "F&R kj", "tanpa_alarm"))
for k, v in out.items():
    print("%-26s %3d %8d %10d %9d %8d %8d %8d %8d %10d" % (
        k, v["n"], v["far_ok_baris"], v["far_ok_kejadian"], v["recall_ok"],
        v["cakupan_ok"], v["ketiga_baris"], v["ketiga_kejadian"],
        v["far_dan_recall_kejadian"], v["fold_tanpa_alarm"]))

# cakupan per fold untuk konteks
print("\ncakupan per fold (baseline hybrid):")
for r in base_j["folds"]:
    if r.get("model") == "hybrid_rule_persistence":
        c = (r.get("cakupan") or {}).get("fraksi")
        print("  %-7s cakupan=%s FAR_kal=%s R=%s" % (
            r["test_well"], c, r.get("far24_kalender"), r["rows"]["recall"]))
