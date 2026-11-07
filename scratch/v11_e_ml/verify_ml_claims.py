#!/usr/bin/env python3
"""V11-E_ML: verifikasi klaim bab ML kandidat 1 & kandidat 2 vs JSON primer."""
import json, os

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch")
eng = {}
for e in ["vib", "ssi", "shk", "stuck_k2"]:
    eng[e] = json.load(open(os.path.join(S, f"v9_e_ML_{e}_RESULTS.json")))
po = json.load(open(os.path.join(S, "v9_e_ML_stuck_k2_persistence_onset.json")))

print("=== A. fold counts, features, kontrak ===")
tot = 0
for e, d in eng.items():
    n = len(d["folds"]); tot += n
    print(f"{e}: folds={n} n_features={d['n_features']} seed={d['seed']} taus={d['taus']}")
    print(f"   ci95={d['ci95_method']}")
    print(f"   jenis_task={d['jenis_task']} | klaim={d['klaim_tugas']}")
    print(f"   hyperparams.rf={d['hyperparams']['rf']}")
    print(f"   hyperparams.gb={d['hyperparams']['gb']}")
    print(f"   hyperparams.lr={d['hyperparams']['lr']}")
    print(f"   software={d['software']}")
print("TOTAL folds =", tot)

fcols = {e: d["feature_cols"] for e, d in eng.items()}
print("feature list identical 4 engines:", all(fcols[e] == fcols["vib"] for e in fcols))
print("n feature_cols:", {e: len(v) for e, v in fcols.items()})

print("\n=== B. agregat RF vs tabel kandidat 2 ===")
K2 = {"vib": (0.4405, 0.9117, 0.4712, "4/4", "2/4"),
      "ssi": (0.0151, 0.4589, 0.4438, "5/7", "6/7"),
      "shk": (0.0069, 0.1929, 0.1860, "5/9", "4/9"),
      "stuck_k2": (0.0697, 0.4443, 0.3747, "4/4", "0/4")}
for e, d in eng.items():
    a = d["agregat"]["rf"]
    print(f"{e}: json min={a['auprc_min']:.4f} max={a['auprc_max']:.4f} spread={a['spread_auprc']:.4f} "
          f"canary={a['deltaB_vs_canary_pos']} pers={a['deltaB_vs_persistence_pos']}")
    print(f"        K2  min={K2[e][0]} max={K2[e][1]} spread={K2[e][2]} canary={K2[e][3]} pers={K2[e][4]}")
    for m in ("gb", "lr"):
        g = d["agregat"][m]
        print(f"   {m}: min={g['auprc_min']:.4f} max={g['auprc_max']:.4f} spread={g['spread_auprc']:.4f} "
              f"canary={g['deltaB_vs_canary_pos']} pers={g['deltaB_vs_persistence_pos']}")

print("\n=== C. baris per fold (primer) ===")
for e, d in eng.items():
    for f in d["folds"]:
        m, b = f["models"], f["baselines"]
        ci = m["rf"]["ci95"]
        print(f"{e} fold{f['fold']} {f['test_well']} n={f['n_test']} pos={f['pos_test']} "
              f"prev={f['prev_test']:.4f} UP={f['underpowered']} "
              f"RF={m['rf']['auprc']:.4f} CI=[{ci[0]:.4f};{ci[1]:.4f}] "
              f"GB={m['gb']['auprc']:.4f} LR={m['lr']['auprc']:.4f} "
              f"pers={b['persistence']['auprc']:.4f} canary={b['canary_depth']['auprc']:.4f} "
              f"rand={b['prevalence_random']['auprc']:.4f}")

print("\n=== D. RF lift per fold vib (K2: 1.61/2.36/3.50/1.63) ===")
print([round(f["models"]["rf"]["lift"], 4) for f in eng["vib"]["folds"]])

print("\n=== E. persistence-onset primer ===")
print(json.dumps(po, indent=1))

print("\n=== F. hitung klaim shk: titik FAR<=60 dari 135 ===")
shk = eng["shk"]
pts = 0; far60 = 0; far6_r_gt0 = []
for f in shk["folds"]:
    for mname in ("rf", "gb", "lr"):
        for tau, tm in f["models"][mname]["tau_metrics"].items():
            pts += 1
            far = tm["FAR_24jam"]
            if far is not None and far <= 60:
                far60 += 1
            if far is not None and far <= 6 and (tm["recall"] or 0) > 0:
                far6_r_gt0.append((f["test_well"], mname, tau, round(far, 2), round(tm["recall"], 4)))
print("shk titik tau =", pts, "| FAR<=60:", far60, "| FAR<=6 & R>0:", far6_r_gt0)

print("\n=== G. hitung klaim 402 titik uji & 10 titik FAR<=6 R>0 (semua engine, termasuk q95) ===")
tot_pts = 0; hits = []
for e, d in eng.items():
    for f in d["folds"]:
        for mname in ("rf", "gb", "lr"):
            for tau, tm in f["models"][mname]["tau_metrics"].items():
                tot_pts += 1
                far = tm["FAR_24jam"]
                if far is not None and far <= 6 and (tm["recall"] or 0) > 0:
                    hits.append((e, f["test_well"], mname, tau, round(far, 2), round(tm["recall"], 4)))
print("total titik tau =", tot_pts, "| FAR<=6 & R>0:", len(hits))
for h in hits:
    print("   ", h)

print("\n=== H. delta_B per fold RF (untuk tabel delta kandidat 2) ===")
for e, d in eng.items():
    for f in d["folds"]:
        db = f["delta_B"]
        print(f"{e} fold{f['fold']} {f['test_well']}: RF-pers={db['rf_vs_persistence']:+.4f} "
              f"RF-canary={db['rf_vs_canary_depth']:+.4f} RF-prev={db['rf_vs_prevalence_random']:+.4f}")

print("\n=== I. stuck_k2 B1/TLead RF q95 + onset persistence ===")
sk = eng["stuck_k2"]
for f in sk["folds"]:
    for mname in ("rf", "gb", "lr"):
        o = f["models"][mname]["onset_by_tau"]["q95_train"]
        print(f"{f['test_well']} {mname} q95: B1={o.get('B1_coverage')} "
              f"TLead={o.get('TLead_median_mnt')} deteksi={o.get('n_detected')}/{o.get('n_events')}")

print("\n=== J. determinism + underpowered + assert/anti-circular meta ===")
for e, d in eng.items():
    print(e, "determinism_check:", d.get("determinism_check"))
    ups = [(f["test_well"], f["pos_test"]) for f in d["folds"] if f["underpowered"]]
    print("   underpowered folds:", ups)
    print("   dataset rows:", d["dataset"], d.get("dataset_sha256", "")[:16])
