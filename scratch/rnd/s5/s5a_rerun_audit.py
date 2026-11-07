#!/usr/bin/env python3
"""AUDIT S5 - rerun dua seed S1 (42 dan 13) memakai harness, bandingkan ke dokumen.

Auditor independen: tidak menulis ke artefak S1, semua keluaran ke scratch/rnd/s5.
"""
import hashlib
import json
import os
import re
import statistics
import sys

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import rnd_hybrid_harness as H  # noqa: E402

OUT = f"{BASE}/scratch/rnd/s5"
DOC = f"{BASE}/docs/RND_S1_SEED_ROBUSTNESS.md"
S1AR = f"{BASE}/scratch/rnd/s1/s1_hyd_seeds.json"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"
LOWO = f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"

SEEDS = (42, 13)
TOL = 5e-5  # setengah digit terakhir (dokumen 4 desimal); pengunci diuji bisa gagal


def sha256(path, blok=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(blok), b""):
            h.update(b)
    return h.hexdigest()


def num(s):
    s = s.strip().replace(".", "").replace(",", ".") if re.search(r"\d,\d", s) else s.strip()
    s = s.replace(" ", "")
    try:
        return float(s)
    except ValueError:
        return None


def tabel(doc):
    """Ambil blok tabel markdown: (baris_header, [sel], [baris_data], no_awal)."""
    lines = doc.splitlines()
    blocks, cur = [], []
    start = 0
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("|"):
            if not cur:
                start = i
            cur.append(l)
        else:
            if cur:
                blocks.append((start, cur))
                cur = []
    if cur:
        blocks.append((start, cur))
    out = []
    for start, blk in blocks:
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in blk]
        header = rows[0]
        body = [r for r in rows[1:] if not re.match(r"^:?-+:?$", r[0].replace(" ", ""))]
        out.append(dict(line=start, header=header, rows=body))
    return out


def cari(blocks, pred):
    for b in blocks:
        if pred(b["header"]):
            return b
    return None


def main():
    doc = open(DOC, encoding="utf-8").read()
    blocks = tabel(doc)

    # ---------------------------------------------------------- 1. dataset
    df = H.muat_dataset(DS)
    well_df = H.pecah_well(df)
    folds = H.muat_fold(LOWO)
    ds = dict(
        path=DS,
        bytes=os.path.getsize(DS),
        sha256_16=sha256(DS)[:16],
        rows=int(df.shape[0]),
        cols=int(df.shape[1]),
        n_well=int(len(well_df)),
        n_fold=int(len(folds)),
    )

    # tabel bagian 3: Well | Baris | Positif | Menit kalender | Cakupan
    t3 = cari(blocks, lambda h: h[:2] == ["Well", "Baris"])
    per_well = []
    for r in (t3["rows"] if t3 else []):
        w = r[0]
        d = well_df[w]
        ts = d["ts_bin"].to_numpy(int)
        menit = int(ts.max() - ts.min() + 1)
        rec = dict(well=w, baris_doc=int(num(r[1])), baris_ukur=int(len(d)),
                   pos_doc=int(num(r[2])), pos_ukur=int(d["y_hyd"].sum()),
                   menit_doc=int(num(r[3])), menit_ukur=menit,
                   cakupan_doc=num(r[4]), cakupan_ukur=round(len(ts) / menit, 4))
        rec["delta_baris"] = rec["baris_ukur"] - rec["baris_doc"]
        rec["delta_pos"] = rec["pos_ukur"] - rec["pos_doc"]
        rec["delta_menit"] = rec["menit_ukur"] - rec["menit_doc"]
        rec["delta_cakupan"] = (None if rec["cakupan_ukur"] is None or rec["cakupan_doc"] is None
                                else round(rec["cakupan_ukur"] - rec["cakupan_doc"], 4))
        per_well.append(rec)

    # ------------------------------------------------------- 2. rerun H1
    rerun = {}
    for s in SEEDS:
        rec = H.jalankan_h1(seed=s, well_df=well_df, folds=folds)
        ring = H.ringkas_records(rec, model="H1_stat_dan_rule")
        rerun[str(s)] = dict(seed=s, ringkas=ring, folds=rec)

    # --------------------------------------- 3. banding dokumen bagian 5.1
    t51 = cari(blocks, lambda h: h and h[0] == "Metrik" and "42" in h)
    banding51 = []
    if t51:
        idx = {s: t51["header"].index(str(s)) for s in SEEDS}
        for r in t51["rows"]:
            met = r[0]
            for s in SEEDS:
                vd = num(r[idx[s]])
                vu = rerun[str(s)]["ringkas"].get(met)
                d = None if (vd is None or vu is None) else round(vu - vd, 6)
                banding51.append(dict(metrik=met, seed=s, dokumen=vd, ukur_ulang=vu,
                                      selisih=d,
                                      lulus=(d is not None and abs(d) <= TOL)))

    # ------------------------------------- 4. banding per fold bagian 4 t2
    t4 = cari(blocks, lambda h: h[:2] == ["Fold", "FP R8"])
    banding_pert4 = []
    if t4:
        hd = t4["header"]
        for r in t4["rows"]:
            fold = r[0]
            row = next((x for x in rerun["42"]["folds"] if x["fold"] == fold and x["model"] == "H1_stat_dan_rule"), None)
            if row is None:
                continue
            pas = [("FP", num(r[1]), row["rows"]["fp"]), ("TP", num(r[4]), row["rows"]["tp"]),
                   ("h", num(r[7]), row["h_terpilih"])]
            for nama, vd, vu in pas:
                banding_pert4.append(dict(fold=fold, metrik=nama, dokumen=vd, ukur_ulang=vu,
                                          selisih=None if vd is None else round(vu - vd, 6),
                                          lulus=(vd is not None and abs(vu - vd) <= 1e-9)))
        _ = hd

    # ----------------------------------- 5. banding lapisan A bagian 6.1
    t61 = cari(blocks, lambda h: h and h[0] == "Fold" and "Cakupan" in h)
    banding61 = []
    if t61:
        hd = t61["header"]
        kol = {"TP": "tp", "FP": "fp", "Presisi": "precision", "Recall": "recall",
               "Lead median": "lead", "Diperingatkan": "diperingatkan"}
        for r in t61["rows"]:
            fold = r[0]
            row = next((x for x in rerun["42"]["folds"] if x["fold"] == fold and x["model"] == "H1_stat_dan_rule"), None)
            if row is None:
                continue
            uji = []
            for nama, kunci in kol.items():
                if nama not in hd:
                    continue
                vd = num(r[hd.index(nama)])
                if kunci == "tp":
                    vu = row["rows"]["tp"]
                elif kunci == "fp":
                    vu = row["rows"]["fp"]
                elif kunci == "precision":
                    vu = row["rows"]["precision"]
                elif kunci == "recall":
                    vu = row["rows"]["recall"]
                elif kunci == "lead":
                    vu = row["lead"]["lead_median_min"]
                else:
                    vu = row["lead"]["n_diperingatkan"]
                uji.append((nama, vd, vu))
            for nama, kunci in (("FAR24 kalender", "far24_kalender"), ("FAR24 baris", "far24_baris"),
                                ("Cakupan", "cakupan"), ("h", "h_terpilih")):
                if nama not in hd:
                    continue
                uji.append((nama, num(r[hd.index(nama)]),
                            row["h_terpilih"] if kunci == "h_terpilih" else row[kunci]))
            for nama, vd, vu in uji:
                banding61.append(dict(fold=fold, metrik=nama, dokumen=vd, ukur_ulang=vu,
                                      selisih=None if (vd is None or vu is None) else round(vu - vd, 6),
                                      lulus=(vd is not None and vu is not None and abs(vu - vd) <= TOL)))

    # ------------------------- 6. aritmetika FAR dihitung ulang dari nol
    arit = []
    for s in SEEDS:
        for r in rerun[str(s)]["folds"]:
            if r["model"] != "H1_stat_dan_rule":
                continue
            fp = r["rows"]["fp"]
            neg = r["menit_neg_kalender"]
            ulang = round(fp / (neg / 1440.0), 4)
            arit.append(dict(seed=s, fold=r["fold"], far_dilaporkan=r["far24_kalender"],
                             far_hitung_ulang=ulang,
                             selisih=round(r["far24_kalender"] - ulang, 6)))

    # -------------------- 7. banding artefak S1 sendiri (bukan dokumen)
    s1 = json.load(open(S1AR, encoding="utf-8"))
    banding_s1ar = []
    for s in SEEDS:
        k = "H1::seed=%d" % s if ("H1::seed=%d" % s) in s1 else None
        bila = s1.get("per_seed", {}).get(str(s), {}).get("ringkas")
        if bila is None:
            continue
        for met, vd in bila.items():
            vu = rerun[str(s)]["ringkas"].get(met)
            if isinstance(vd, (int, float)) and isinstance(vu, (int, float)):
                banding_s1ar.append(dict(seed=s, metrik=met, artefak=vd, ukur_ulang=vu,
                                         selisih=round(vu - vd, 6),
                                         lulus=abs(vu - vd) <= TOL))
        _ = k

    hasil = dict(
        waktu_run=pd.Timestamp.now(tz="Asia/Jakarta").isoformat(),
        dataset=ds, per_well=per_well,
        rerun={"%s" % s: dict(ringkas=rerun[str(s)]["ringkas"],
                              folds=[{k: v for k, v in r.items() if k in
                                      ("fold", "model", "h_terpilih", "cal_well", "n", "n_pos",
                                       "far24_kalender", "far24_baris", "cakupan", "menit_kalender",
                                       "menit_neg_kalender", "gate_A_baru")} |
                                      dict(tp=r["rows"]["tp"], fp=r["rows"]["fp"],
                                           precision=r["rows"]["precision"], recall=r["rows"]["recall"],
                                           lead_median=r["lead"]["lead_median_min"],
                                           n_onset=r["lead"]["n_onset"],
                                           n_diperingatkan=r["lead"]["n_diperingatkan"])
                                      for r in rerun[str(s)]["folds"] if r["model"] == "H1_stat_dan_rule"])
                              for s in SEEDS},
        banding_dok_51=banding51, banding_dok_4_perfold=banding_pert4,
        banding_dok_61=banding61, aritmetika_far=arit, banding_artefak_s1=banding_s1ar,
    )
    os.makedirs(OUT, exist_ok=True)
    H.tulis_json(f"{OUT}/s5_rerun_audit.json", hasil)

    print("dataset:", ds)
    print("per well delta (baris/pos/menit/cakupan) nol semua:",
          all(p["delta_baris"] == 0 and p["delta_pos"] == 0 and p["delta_menit"] == 0
              and p["delta_cakupan"] in (0, 0.0, None) for p in per_well),
          "| n well:", len(per_well))
    for s in SEEDS:
        r = rerun[str(s)]["ringkas"]
        print(f"seed {s}: fp {r['fp_total']} tp {r['tp_total']} prec {r['precision_median']} "
              f"rec {r['recall_median']} far24kal {r['far24_kalender_median']} lead {r['lead_median_median']}")
    for nama, blk in (("5.1", banding51), ("4-perfold", banding_pert4), ("6.1", banding61)):
        gagal = [b for b in blk if not b["lulus"]]
        print(f"banding dok {nama}: n={len(blk)} gagal={len(gagal)}")
        for g in gagal[:8]:
            print("   ", g)
    print("aritmetika FAR: n=", len(arit), "menyimpang=",
          sum(1 for a in arit if abs(a["selisih"]) > 1e-9))
    gagal = [b for b in banding_s1ar if not b["lulus"]]
    print("banding artefak S1: n=", len(banding_s1ar), "gagal=", len(gagal),
          gagal[:5])


if __name__ == "__main__":
    main()
