#!/usr/bin/env python3
"""V9-I1 — DRIVER: replay SATU segmen data Volve ke alat PdM advisory (7 engine).

Pemakaian:
    python3 code/v9_i1_run.py                 # replay F-14 tanpa head ML
    python3 code/v9_i1_run.py --ml            # + 4 RF head (LOWO, seed 42)
    python3 code/v9_i1_run.py --well F-14 --ml

Output:
    scratch/v9_i1/v9_i1_RESULTS.json   — JSON primer (S6: json dulu, dokumen kemudian)
    scratch/v9_i1/v9_i1_RUN_LOG.txt    — run log bertimestamp
    stdout                             — laporan manusia (status + peringatan + skor)

Yang dihormati prototipe ini:
  * tier tiap head = tier EVAL_C (I1 tidak menaikkan tier) — diverifikasi v9_i1_verify.py;
  * output L2 (engine tren) TIDAK pernah jadi peringatan — assertion di decision_layer;
  * semua peringatan L1 membawa human_review_required=true + badge FAR + batas tertulis;
  * klaim yang belum tersedia (hyd K-ii, bit_wear K-2, tool_wear K-ii RF) ditulis
    eksplisit sebagai status — bukan skor 0.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v9_i1_pipeline as P  # noqa: E402


def log_factory(fp):
    def log(msg):
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        print(line, flush=True)
        fp.write(line + "\n")
        fp.flush()
    return log


def load_rig(well: str) -> tuple[dict, dict]:
    """Muat dataset rig TWICE: (segmen = well tujuan) + (FULL = utk latih LOWO)."""
    seg, full = {}, {}
    for key in ["vib", "ssi", "shk", "stuck_k1", "stuck_k2", "hyd_ki"]:
        df = pd.read_csv(f"{P.DS}/{key}.csv.gz")
        full[key] = df.sort_values(["well", "ts_bin"]).reset_index(drop=True)
        seg[key] = (df[df["well"] == well].sort_values("ts_bin")
                    .reset_index(drop=True))
    return seg, full


def seg_info(df: pd.DataFrame, ts_col: str = "ts_bin") -> dict:
    if len(df) == 0:
        return {"n": 0}
    ts = df[ts_col].to_numpy().astype("int64")
    span = int(ts.max() - ts.min() + 1)
    return {"n": int(len(df)),
            "ts_bin_min": int(ts.min()), "ts_bin_max": int(ts.max()),
            "rentang_menit": span,
            "catatan_waktu": "ts_bin = indeks menit internal D1 (grid 60 dtk, "
                             "+1 per menit); asal kalender TIDAK diverifikasi di "
                             "sesi ini — jangan dibaca sebagai tanggal"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--well", default="F-14")
    ap.add_argument("--ml", action="store_true",
                    help="jalankan 4 RF head (LOWO seed 42)")
    ap.add_argument("--outdir", default=P.OUTDIR)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    res_path = f"{args.outdir}/v9_i1_RESULTS.json"
    log_path = f"{args.outdir}/v9_i1_RUN_LOG.txt"
    fp = open(log_path, "a")
    log = log_factory(fp)
    t0 = time.time()
    log("=" * 78)
    log(f"V9-I1 RUN mulai | segmen rig = {args.well} | ML={'ON' if args.ml else 'OFF'}")
    log(f"python={sys.version.split()[0]} numpy={np.__version__} pandas={pd.__version__}")

    # ---- Layer-0/1: muat segmen ----
    rig, rig_full = load_rig(args.well)
    for k, df in rig.items():
        log(f"muat {k}: n={len(df)} {seg_info(df)} | full(all well) n={len(rig_full[k])}")
        assert len(df) > 0, f"segmen {args.well} kosong di dataset {k}"
    r01, r02 = P.rule_modules()
    log(f"impor modul kampanye E_RULE: {os.path.basename(r01.__file__)} + "
        f"{os.path.basename(r02.__file__)}")

    engines = []

    # ---- 7 ENGINE ----
    log("engine 1/7 vib ...")
    engines.append(P.run_vib(rig["vib"], rig_full["vib"], r01, args.ml))
    log("engine 2/7 ssi ...")
    engines.append(P.run_ssi(rig["ssi"], rig_full["ssi"], r01, args.ml))
    log("engine 3/7 shk ...")
    engines.append(P.run_shk(rig["shk"], rig_full["shk"], r01, args.ml))
    log("engine 4/7 stuck (K-i + K-ii) ...")
    engines.append(P.run_stuck(rig["stuck_k1"], rig["stuck_k2"],
                               rig_full["stuck_k2"], r01, r02, args.ml))
    log("engine 5/7 hyd (K-i; K-ii = belum tersedia, ditulis eksplisit) ...")
    engines.append(P.run_hyd(rig["hyd_ki"], r01))

    log("engine 6/7 bit_wear (USROP, grid Kedalaman) ...")
    usrop = pd.read_csv(P.USROP)
    usrop_seg = usrop[usrop["well"].str.contains(args.well.replace("-", ""), regex=False)
                      | (usrop["well"] == f"USROP_A 2 N-SH_{args.well}d.csv")]
    if len(usrop_seg) == 0:  # fallback eksplisit: segmen F-14 USROP
        usrop_seg = usrop[usrop["well"].str.contains("_F-14", regex=False)]
    log(f"USROP segmen: well={sorted(usrop_seg['well'].unique())} n={len(usrop_seg)}")
    assert len(usrop_seg) > 0, "segmen USROP tidak ditemukan"
    engines.append(P.run_bit_wear(usrop_seg))

    log("engine 7/7 tool_wear (modul bengkel — domain terpisah) ...")
    tw = pd.read_csv(P.TOOLWEAR)
    engines.append(P.run_tool_wear(tw))

    # ---- Layer-3: lapisan keputusan + profil kapabilitas + nilai maintenance ----
    log("lapisan keputusan (L1 wajib review manusia) ...")
    decision = P.decision_layer(engines)
    log(f"ringkasan layer: {decision['ringkasan']} | peringatan L1 = {decision['nperingatan_l1']}")

    log("profil kapabilitas per engine (lapisan A/B/C) ...")
    kapabilitas = P.profil_kapabilitas(engines)

    log("nilai maintenance dari data aktivitas DDR (jam henti, beban tinjauan) ...")
    nilai = P.nilai_maintenance(engines)
    log(f"aktivitas DDR: {nilai.get('n_record_aktivitas')} record, {nilai.get('total_jam_tercatat')} jam tercatat")

    results = {
        "meta": {
            "task": "t_34e9b879 V9-I1 prototipe alat PdM advisory",
            "segmen_rig": args.well,
            "segmen_usrop": sorted(usrop_seg["well"].unique().tolist()),
            "segmen_tool_wear": f"{tw['tool'].nunique()} alat x 2 run ({len(tw)} jendela)",
            "ml": bool(args.ml),
            "seed": P.SEED,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_s": None,
            "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 (I1 tidak mengubah tier)",
            "n_engine": len(engines),
        },
        "segmen_info": {k: seg_info(v) for k, v in rig.items()},
        "engines": engines,
        "decision_layer": decision,
        "profil_kapabilitas": kapabilitas,
        "nilai_maintenance": nilai,
        "human_review_required": True,
        "keputusan_akhir": "MANUSIA — alat ini menyiapkan status, peringatan, tren, dan bahan rencana inspeksi",
    }

    # ---- laporan manusia (stdout) ----
    print()
    print("=" * 78)
    print(f"ALAT PdM ADVISORY — PROTOTIPE V9-I1 | segmen rig {args.well}")
    print("=" * 78)
    for e in engines:
        print(f"\n[{e['engine']}] {e['klaim_tugas']}")
        print(f"    jenis tugas : {e['jenis_tugas']}")
        print(f"    sumber tier : {e['sumber_tier']}")
        if e.get("catatan_klaim"):
            print(f"    catatan     : {e['catatan_klaim']}")
        if e.get("domain"):
            print(f"    domain      : {e['domain']}")
        for h in e["heads"]:
            akt = h.get("n_aktif")
            met = h.get("metrik_segmen") or {}
            print(f"  - {h['head']:<30} tier={h['tier']:<24} layer={h['layer']}")
            if h.get("status"):
                print(f"      status        : {h['status']}")
            if akt is not None:
                print(f"      aktif         : {akt}/{h['n_windows']} "
                      f"({h.get('frac_aktif', 0):.3f})")
            if met:
                print(f"      metrik segmen : P={met['precision']} R={met['recall']} "
                      f"FP={met['fp']} FARseg={met['far_segmen']} [{met['far_unit']}]")
            if h.get("auprc_segmen") is not None:
                print(f"      AUPRC segmen  : {h['auprc_segmen']}")
            print(f"      badge FAR     : {h['badge_far']}")
            print(f"      keyakinan     : {h['keyakinan']}")
            print(f"      batas         : {h['batas_pemakaian']}")
            print(f"      human review  : {h['human_review_required']}")

    print("\n" + "=" * 78)
    print("LAPISAN KEPUTUSAN")
    for k in ["L0", "L1", "L2", "L3"]:
        items = decision["layers"][k]
        print(f"  {k} {P.LAYERS[k]}: {len(items)} head")
        for it in items:
            print(f"      · {it['engine']}/{it['head']} [{it['tier']}]"
                  + (f" status={it['status']}" if it.get("status") else "")
                  + (f" n_aktif={it['n_aktif']}" if it.get("n_aktif") is not None else ""))
    print(f"\n  Peringatan L1 (butuh konfirmasi manusia): {decision['nperingatan_l1']}")
    print(f"  Keputusan akhir: {decision['keputusan_akhir']}")
    print(f"  human_review_required: WAJIB (seluruh peringatan L1 & daftar L3)")

    print("\n" + "=" * 78)
    print("NILAI MAINTENANCE (dari data aktivitas DDR, bukan asumsi)")
    print(f"  record aktivitas      : {nilai.get('n_record_aktivitas')}")
    print(f"  total jam tercatat    : {nilai.get('total_jam_tercatat')}")
    top = list((nilai.get("jam_per_kode") or {}).items())[:5]
    for k, v in top:
        print(f"    · {k:<28} {v} jam")
    print("  beban tinjauan per shift 8 jam (head L1, dari FAR segmen):")
    for b in nilai.get("beban_tinjauan_L1", [])[:8]:
        print(f"    · {b['engine']}/{b['head']:<28} FAR/24j={b['far_per_24jam']:<8} "
              f"tinjauan/shift={b['tinjauan_per_shift_8jam']}")
    print(f"  batas: {nilai.get('batas')}")

    print("\n" + "=" * 78)
    print("PROFIL KAPABILITAS (A deteksi, B nilai maintenance, C ketepatan)")
    for pr in kapabilitas:
        A = pr["lapisan_A_deteksi"]; B = pr["lapisan_B_nilai_maintenance"]
        print(f"  [{pr['engine']}] {pr['jenis_tugas']}")
        print(f"     A: head bermetrik={A['head_dengan_metrik']} P={A['presisi_maks']} "
              f"R={A['recall_maks']} FARmin={A['far_min']}")
        print(f"     B: {B['status']}" + (f" ({B['alasan']})" if B.get('alasan') else ""))
        print(f"     C: layer L1={len(pr['lapisan_C_ketepatan']['head_peringatan_L1'])} head, "
              f"kekuatan bukti={pr['kekuatan_bukti']}")
    print("=" * 78)

    results["meta"]["elapsed_s"] = round(time.time() - t0, 2)
    with open(res_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    log(f"JSON primer ditulis: {res_path} ({os.path.getsize(res_path)} byte)")
    log(f"selesai dalam {results['meta']['elapsed_s']} s")
    fp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
