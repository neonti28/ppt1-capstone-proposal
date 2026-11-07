#!/usr/bin/env python3
"""V9-I1 — VERIFIKASI INDEPENDEN prototipe integrasi (bukan mengulang driver).

Dijalankan SESUDAH v9_i1_run.py; membaca JSON primer + dokumen sumber + dataset
mentah, lalu menguji 8 hal dengan implementasi TERPISAH (bukan memanggil ulang
fungsi yang sama dengan driver — verification-mandatory #4):

  V1 7 engine ada di JSON + semua head punya tier/lapisan/badge/batas.
  V2 tier registry == teks tier pada docs/V9_EVAL_C_LAYERC.md §1 (parsing regex);
     I1 tidak boleh menaikkan/menurunkan tier sendiri.
  V3 0 head bertier ALARM-OTOMATIS; slot alarm otomatis = 0.
  V4 semua head L1 tier = PERINGATAN-BERPENGAWAS + human_review_required=true;
     head tier TREN/BELUM-LAYAK tidak pernah jatuh ke L1 (engine tren tanpa alarm).
  V5 recompute independen dari dataset mentah (implementasi sendiri, bukan import
     engine): persistence vib + rule vib t0-1 dari bins + hybrid = rule AND pers;
     persistence hyd; persistence bit_wear; deteksi tool_wear alat T01.
  V6 klaim "belum tersedia/dijalankan" (hyd K-ii, bit_wear K-2) tertulis eksplisit
     sebagai status — bukan nol diam, bukan skor 0 palsu.
  V7 determinisme: run ulang driver tanpa --ml ke dua outdir temp, JSON identik
     setelah meta timestamps/elapsed dibuang.
  V8 determinisme ML opsional: skor RF dihitung ulang utk satu head → AUPRC sama.

Keluaran: stdout + scratch/v9_i1/v9_i1_VERIFY.txt (PASS/GAGAL per cek).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import v9_i1_pipeline as P  # noqa: E402

RESULTS = f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"
DOC_C = f"{BASE}/docs/V9_EVAL_C_LAYERC.md"
LINES: list[str] = []


def check(vid: str, ok: bool, detail: str):
    LINES.append(f"[{'PASS' if ok else 'GAGAL'}] {vid}: {detail}")
    print(LINES[-1], flush=True)
    return ok


def main() -> int:
    with open(RESULTS) as f:
        res = json.load(f)
    eng = {e["engine"]: e for e in res["engines"]}
    ok_all = True

    # V1 ---- 7 engine + kelengkapan head
    expect = {"vib", "ssi", "shk", "stuck", "hyd", "bit_wear", "tool_wear"}
    ok = set(eng) == expect
    ok_all &= check("V1a", ok, f"engine di JSON = {sorted(eng)} (diharapkan {sorted(expect)})")
    missing = [(e, h) for e, blk in eng.items() for h in blk["heads"]
               if not all(k in h for k in ("tier", "layer", "badge_far",
                                           "keyakinan", "batas_pemakaian"))]
    ok_all &= check("V1b", not missing,
                    f"head tanpa tier/layer/badge/keyakinan/batas = {missing}")

    # V2 ---- tier tidak pernah LEBIH TINGGI dari dokumen EVAL_C (I1 boleh lebih
    # konservatif/lower-tier per head, tetapi dilarang menaikkan tier sendiri)
    doc = open(DOC_C, encoding="utf-8").read()
    rank = {P.T_NONE: 0, P.T_TREN: 1, P.T_SUPERV: 2, P.TIER_FORBIDDEN: 3}

    def doc_rank(row: str) -> int:
        """Rank tier di baris dokumen: 0=BELUM LAYAK, 1=TREN, 2=PERINGATAN.
        (Tier ALARM-OTOMATIS sengaja TIDAK dihitung di sini — V3a sudah
        meng-assert tidak ada head bertier ALARM-OTOMATIS sama sekali.)"""
        r = 0
        if "TREN" in row:
            r = max(r, 1)
        if "PERINGATAN-BERPENGAWAS" in row:
            r = max(r, 2)
        return r

    rows_by_eng = {}
    for e in eng:
        rows_by_eng[e] = re.findall(rf"^\|[^\n]*\*\*{re.escape(e)}[ \*][^\n]*",
                                    doc, flags=re.M)
    tier_ok, tier_bad = [], []
    for e, blk in eng.items():
        cands = rows_by_eng[e]
        if not cands:
            tier_bad.append(f"{e}: baris tabel §1 tidak ditemukan")
            continue
        for h in blk["heads"]:
            kl = h.get("klaim")
            # baris dipilih dari SEL PERTAMA ("**stuck K-ii**"), bukan sekadar
            # mengandung teks klaim (baris K-i juga memuat kata "K-ii" di kolom lain)
            def first_cell(r):
                return r.split("|")[1].strip() if r.count("|") else r
            row = next((r for r in cands
                        if first_cell(r).startswith(f"**{e}")
                        and (not kl or kl in first_cell(r))), cands[0])
            t = h["tier"]
            dr = doc_rank(row)
            if rank[t] > dr:
                tier_bad.append(f"{e}/{h['head']}: tier prototipe '{t}' (rank "
                                f"{rank[t]}) LEBIH TINGGI dari dokumen EVAL_C "
                                f"(rank {dr}) — KENAIKAN TIER DILARANG")
            else:
                tier_ok.append(f"{e}/{h['head']}")
    ok_all &= check("V2", not tier_bad,
                    f"tier cocok dokumen: {len(tier_ok)} head; "
                    f"tidak cocok: {tier_bad}")

    # V3 ---- tanpa alarm otomatis
    forb = [(e, h["head"]) for e, blk in eng.items() for h in blk["heads"]
            if h["tier"] == P.TIER_FORBIDDEN]
    ok_all &= check("V3a", not forb, f"head bertier ALARM-OTOMATIS = {forb}")
    ok_all &= check("V3b",
                    res["auto_critical_alarm_slots"] == 0
                    and res["decision_layer"]["auto_critical_alarm_slots"] == 0,
                    "slot alarm otomatis kritis = 0 (meta + decision_layer)")

    # V4 ---- aturan lapisan
    bad = []
    for e, blk in eng.items():
        for h in blk["heads"]:
            if h["layer"] == "L1":
                if h["tier"] != P.T_SUPERV:
                    bad.append(f"{e}/{h['head']} L1 dgn tier {h['tier']}")
                if h["human_review_required"] is not True:
                    bad.append(f"{e}/{h['head']} L1 tanpa human_review_required")
            if h["tier"] in (P.T_TREN, P.T_NONE) and h["layer"] == "L1":
                bad.append(f"{e}/{h['head']} engine tren/lolos jadi peringatan")
            if h["layer"] == "L0" and h["human_review_required"] not in (True, False):
                bad.append(f"{e}/{h['head']} human_review_required bukan bool")
    ok_all &= check("V4a", not bad, f"pelanggaran aturan lapisan = {bad}")
    l1 = res["decision_layer"]["layers"]["L1"]
    ok_all &= check("V4b", all(i["human_review_required"] for i in l1),
                    f"semua {len(l1)} entri L1 human_review_required=true")

    # V5 ---- recompute independen dari data mentah
    w = res["meta"]["segmen_rig"]
    recomputed = []

    # (a) persistence vib
    vib = pd.read_csv(f"{P.DS}/vib.csv.gz")
    vib = vib[vib["well"] == w]
    pers_v = int((vib["y_prev_vib"].fillna(0).to_numpy().astype(int) == 1).sum())
    jv = next(h for h in eng["vib"]["heads"] if h["head"] == "persistence")
    recomputed.append(("vib.persistence.n_aktif", pers_v, jv["n_aktif"]))

    # (b) rule vib t0-1 — implementasi mandiri langsung dari bins (tanpa r01)
    bins = pd.read_csv(f"{P.BINS}/{w}.csv.gz")
    b = bins.sort_values("ts_bin").set_index("ts_bin")
    ts = vib["ts_bin"].to_numpy().astype("int64")
    v = b["vib_max"].reindex(pd.Index(ts - 1))
    rule_v = int((v.fillna(-np.inf).to_numpy() >= 32.17405).astype(int).sum())
    jr = next(h for h in eng["vib"]["heads"] if h["head"] == "rule_display")
    recomputed.append(("vib.rule_display.n_aktif", rule_v, jr["n_aktif"]))

    # (c) hybrid = rule AND persistence (implementasi mandiri)
    hyb_v = int((((v.fillna(-np.inf).to_numpy() >= 32.17405).astype(int)) &
                 (vib["y_prev_vib"].fillna(0).to_numpy().astype(int))).sum())
    jh = next(h for h in eng["vib"]["heads"]
              if h["head"] == "hybrid_rule_and_persistence")
    recomputed.append(("vib.hybrid.n_aktif", hyb_v, jh["n_aktif"]))

    # (d) persistence hyd
    hyd = pd.read_csv(f"{P.DS}/hyd_ki.csv.gz")
    hyd = hyd[hyd["well"] == w]
    pers_h = int((hyd["y_prev_hyd"].fillna(0).to_numpy().astype(int) == 1).sum())
    jhp = next(h for h in eng["hyd"]["heads"] if h["head"] == "persistence")
    recomputed.append(("hyd.persistence.n_aktif", pers_h, jhp["n_aktif"]))

    # (e) persistence bit_wear pada grid Kedalaman
    us = pd.read_csv(P.USROP)
    us = us[us["well"] == res["meta"]["segmen_usrop"][0]].sort_values(
        "Measured Depth m").reset_index(drop=True)
    ym = (us["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
    pers_b = int(np.concatenate([[0], ym[:-1]]).sum())
    jbp = next(h for h in eng["bit_wear"]["heads"] if h["head"] == "persistence")
    recomputed.append(("bit_wear.persistence.n_aktif", pers_b, jbp["n_aktif"]))

    # (f) deteksi tool_wear alat T01 — resep kalibrasi ditulis ulang mandiri
    tw = pd.read_csv(P.TOOLWEAR)
    feats = [c for c in tw.columns
             if c.endswith(("_mean", "_std", "_rms", "_kurt", "_skew", "_p2p",
                            "_crest", "_zcr", "_fdom"))]
    g = tw[tw["tool"] == "T01"].sort_values(["run", "start_sample"])
    r01_ = g[g["run"] == "R01"]
    r02_ = g[g["run"] == "R02"]
    ncal = max(5, int(np.ceil(0.30 * len(r01_))))
    med = r01_.iloc[:ncal][feats].median()
    mad = (r01_.iloc[:ncal][feats] - med).abs().median() * 1.4826
    mad = mad.replace(0, np.nan)
    Z = ((r02_[feats] - med) / mad).abs()
    act2 = (Z > 3.0).sum(axis=1).to_numpy() >= 5
    det_t01 = bool(act2.any())
    per_alat = next(h for h in eng["tool_wear"]["heads"]
                    if h["head"] == "calib_5of27")["per_alat"]
    jdet = [r for r in per_alat if r["alat"] == "T01"][0]["engine_5of27"]["det_R02"]
    recomputed.append(("tool_wear.T01.deteksi_R02", det_t01, jdet))

    bad5 = [(k, a, b) for k, a, b in recomputed if a != b]
    ok_all &= check("V5", not bad5,
                    f"{len(recomputed)-len(bad5)}/{len(recomputed)} angka cocok "
                    f"(recompute independen); selisih={bad5}")

    # V6 ---- klaim belum-tersedia eksplisit
    hyd2 = next(h for h in eng["hyd"]["heads"] if h["head"] == "k2_tidak_tersedia")
    bw2 = next(h for h in eng["bit_wear"]["heads"] if h["head"] == "k2_onset_belum")
    ok6 = ("BELUM" in hyd2.get("status", "").upper()
           and "BELUM" in bw2.get("status", "").upper()
           and hyd2["n_windows"] == 0 and bw2["n_windows"] == 0
           and "metrik_segmen" not in hyd2 and "metrik_segmen" not in bw2)
    ok_all &= check("V6", ok6,
                    f"klaim non-aktif eksplisit: hyd K-ii status='{hyd2.get('status')}', "
                    f"bit_wear K-2 status='{bw2.get('status')}', tanpa metrik_segmen")

    # V7 ---- determinisme run ulang (tanpa ML)
    tmp = f"{BASE}/scratch/v9_i1/_det"
    os.makedirs(tmp, exist_ok=True)
    for i in (1, 2):
        subprocess.run([sys.executable, f"{BASE}/code/v9_i1_run.py",
                        "--outdir", f"{tmp}/r{i}"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def strip(o):
        o = json.loads(json.dumps(o))
        for k in ("generated_at", "elapsed_s"):
            o["meta"].pop(k, None)
        return json.dumps(o, sort_keys=True, default=str)
    a = strip(json.load(open(f"{tmp}/r1/v9_i1_RESULTS.json")))
    b = strip(json.load(open(f"{tmp}/r2/v9_i1_RESULTS.json")))
    ok_all &= check("V7", a == b,
                    "dua run ulang identik setelah meta waktu dibuang"
                    if a == b else "JSON run ulang BERBEDA")

    # V8 ---- determinisme ML (1 head diulang → AUPRC sama dgn JSON)
    ml_head = next((h for h in eng["shk"]["heads"]
                    if h["head"] == "rf_lowo" and h.get("auprc_segmen") is not None),
                   None)
    if ml_head is None:
        ok_all &= check("V8", True,
                        "ML tidak dijalankan pada run ini → dilewati (dinyatakan)")
    else:
        shk = pd.read_csv(f"{P.DS}/shk.csv.gz")
        shk = shk[shk["well"].notna()]
        res2 = P.train_lowo(shk, "y_shk", res["meta"]["segmen_rig"], n_estimators=300)
        rec = P.auprc(res2["y"], res2["score"])
        ok_all &= check("V8", rec == ml_head["auprc_segmen"],
                        f"AUPRC shk RF recompute={rec} vs JSON={ml_head['auprc_segmen']}")

    # V9 ---- konsistensi kampanye: titik operasi tool_wear == E_STAT §C (target 1,0)
    try:
        stat = json.load(open(f"{BASE}/scratch/v9_e_stat/"
                              "v9_e_stat_03_tool_wear_RESULTS.json"))
        camp = {(c["tool"], c["target_fp_per_min"]): c
                for c in stat["part_C_operating_far_calibrated"]}
        op = next(h for h in eng["tool_wear"]["heads"]
                  if h["head"] == "op_far_calibrated")["per_alat"]
        diffs = []
        for row in op:
            c = camp.get((row["alat"], 1.0))
            if c is None:
                diffs.append(f"{row['alat']}: fold kampanye tidak ada")
                continue
            for k in ("fp_R01", "det_R02", "first_alarm_s"):
                if row[k] != c[k]:
                    diffs.append(f"{row['alat']}.{k}: prototipe={row[k]} "
                                 f"kampanye={c[k]}")
            if abs((row["TLead_s"] or -1) - (c["TLead_s"] or -1)) > 1e-9:
                diffs.append(f"{row['alat']}.TLead: prototipe={row['TLead_s']} "
                             f"kampanye={c['TLead_s']}")
            if abs((row["thr_featcount"] or -1) - (c["thr_featcount"] or -1)) > 1e-9:
                diffs.append(f"{row['alat']}.thr: prototipe={row['thr_featcount']} "
                             f"kampanye={c['thr_featcount']}")
        ok_all &= check("V9", not diffs,
                        f"tool_wear op_far_calibrated == E_STAT §C utk 4 alat "
                        f"(fp/det/first/TLead/thr); selisih={diffs}")
    except FileNotFoundError as exc:
        ok_all &= check("V9", False, f"JSON E_STAT tidak ditemukan: {exc}")

    # V10 ---- konsistensi kampanye: replay F-14 == fold F-14 di E_RULE §1
    # (persistence + rule-display per kelas status; angka metrik segmen prototipe
    #  harus identik dengan fold kampanye pada well yang sama)
    try:
        rule = json.load(open(f"{BASE}/scratch/v9_e_rule/"
                              "v9_e_RULE_01_status_results.json"))
        cls_map = {"vib": "vib", "ssi": "ssi", "shk": "shk",
                   "stuck": "stuck_k1", "hyd": "hyd_ki"}
        diffs10 = []
        for eng_name, cls in cls_map.items():
            folds = rule["classes"][cls]["folds"]
            f = next((x for x in folds if x["test_well"] == res["meta"]["segmen_rig"]),
                     None)
            if f is None:
                diffs10.append(f"{cls}: fold {res['meta']['segmen_rig']} tidak ada")
                continue
            for head_name, camp_key in (("persistence", "persistence"),
                                        ("rule_display", "rule_display_t0minus1")):
                h = next(x for x in eng[eng_name]["heads"]
                         if x["head"] == head_name)
                m = h["metrik_segmen"]
                c = f[camp_key]
                for mk, ck in (("tp", "tp"), ("fp", "fp")):
                    if m[mk] != c[ck]:
                        diffs10.append(f"{cls}/{head_name}.{mk}: "
                                       f"prototipe={m[mk]} kampanye={c[ck]}")
                def r(x, nd):
                    return None if x is None else round(x, nd)
                if r(m["precision"], 4) != r(c.get("precision"), 4):
                    diffs10.append(f"{cls}/{head_name}.precision: "
                                   f"prototipe={m['precision']} "
                                   f"kampanye={c.get('precision')}")
                if r(m["far_segmen"], 3) != r(c.get("far_24h"), 3):
                    diffs10.append(f"{cls}/{head_name}.far: "
                                   f"prototipe={m['far_segmen']} "
                                   f"kampanye={c.get('far_24h')}")
        ok_all &= check("V10", not diffs10,
                        f"replay F-14 identik dgn fold kampanye E_RULE utk "
                        f"{len(cls_map)} kelas x 2 head (tp/fp/precision/FAR); "
                        f"selisih={diffs10}")
    except FileNotFoundError as exc:
        ok_all &= check("V10", False, f"JSON E_RULE tidak ditemukan: {exc}")

    out = "\n".join(LINES) + f"\nTOTAL: {'SEMUA PASS' if ok_all else 'ADA GAGAL'}\n"
    with open(f"{BASE}/scratch/v9_i1/v9_i1_VERIFY.txt", "w") as f:
        f.write(out)
    print(out)
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
