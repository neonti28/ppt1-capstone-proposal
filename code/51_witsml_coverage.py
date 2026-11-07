#!/usr/bin/env python3
"""T9 — Coverage: event label (labels_curated_v2.csv) vs rentang time-series WITSML.

Untuk tiap fold: berapa event label jatuh DI DALAM rentang timestamp CSV hasil parse
(overall + union cluster, karena rentang bisa punya gap) -> tabel coverage.

Pemetaan fold -> label wellbore (rantai bukti, lihat laporan §3):
  baris fold (V2_ML_RESULTS §6) == baris file USROP_A N (dihitung ulang)
  file USROP mentah Norway-<prefix>_<well> depth.csv == nama folder WITSML
"""
import csv
import json
import os
from datetime import datetime, timezone

LAB = "/mnt/d/Capstone 1/data/volve/labels_curated_v2.csv"
OUT = "/mnt/d/Capstone 1/data/volve/witsml_parsed"

FOLD2LABEL = {
    "F-9_A":   "NO 15/9-F-9 A",
    "F-7":     "NO 15/9-F-7",
    "F-14":    "NO 15/9-F-14",
    "F-15A":   "NO 15/9-F-15 A",
    "F-15_S":  "NO 15/9-F-15",
    "F-5":     "NO 15/9-F-5",
    "F-9":     "NO 15/9-F-9",
    # varian (bukti pemilihan, bukan fold)
    "VAR_F-15A_folder": "NO 15/9-F-15 A",
    "VAR_F-5_alt":      "NO 15/9-F-5",
}


def parse_iso(s):
    if not s:
        return None
    t = s.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        return None
    # event_date kadang polos (tanpa zona) -> asumsikan UTC (dicatat di laporan)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def main():
    rows = list(csv.DictReader(open(LAB, newline="", encoding="utf-8")))
    labels = {}
    for r in rows:
        labels.setdefault(r["wellbore"], []).append(r)

    out = {}
    print(f"{'fold':18s} {'label wellbore':16s} {'n_lab':>5s} {'n_dated':>7s} "
          f"{'overall':>8s} {'cluster':>8s} {'%clus':>7s}")
    for fold, lab in FOLD2LABEL.items():
        qc_path = os.path.join(OUT, f"{fold}.qc.json")
        if not os.path.exists(qc_path):
            out[fold] = {"status": "QC belum ada"}
            print(f"{fold:18s} {lab:16s}  (belum diparse)")
            continue
        q = json.load(open(qc_path))
        tmin = parse_iso(q.get("t_min_utc"))
        tmax = parse_iso(q.get("t_max_utc"))
        cl = []
        for c in q.get("clusters", []):
            a, b = parse_iso(c["t_min"]), parse_iso(c["t_max"])
            if a and b:
                cl.append((a, b))
        ev = labels.get(lab, [])
        dated = [e for e in ev if parse_iso(e["event_date"])]
        in_overall = sum(1 for e in dated if tmin and tmax
                         and tmin <= parse_iso(e["event_date"]) <= tmax)
        in_cluster = sum(1 for e in dated
                         if any(a <= parse_iso(e["event_date"]) <= b for a, b in cl))
        # cross-check kedua: pakai act_start (timestamp lokal +01/+02 -> UTC)
        in_cluster_act = 0
        for e in ev:
            raw = e.get("act_start") or ""
            if not raw:
                continue
            try:
                dt = datetime.fromisoformat(raw)
            except ValueError:
                continue
            if dt.tzinfo is None or not tmin or not tmax:
                continue
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            a = tmin.replace(tzinfo=None)
            b = tmax.replace(tzinfo=None)
            if a <= dt <= b:
                in_cluster_act += 1
        out[fold] = {
            "label_wellbore": lab, "n_labels": len(ev), "n_labels_dated": len(dated),
            "t_min_utc": q.get("t_min_utc"), "t_max_utc": q.get("t_max_utc"),
            "n_in_overall_range": in_overall, "n_in_cluster_ranges": in_cluster,
            "n_in_overall_via_act_start_utc": in_cluster_act,
            "coverage_pct_cluster": round(100 * in_cluster / len(dated), 1) if dated else None,
            "n_rows_timeseries": q.get("n_rows_final"),
            "folder": q.get("folder"),
            "n_clusters": q.get("n_clusters"),
            "cluster_ranges": [[c["t_min"], c["t_max"], c["rows_written"]]
                               for c in q.get("clusters", [])],
            "event_date_min": min((e["event_date"] for e in dated), default=None),
            "event_date_max": max((e["event_date"] for e in dated), default=None),
        }
        print(f"{fold:18s} {lab:16s} {len(ev):5d} {len(dated):7d} "
              f"{in_overall:8d} {in_cluster:8d} "
              f"{(100 * in_cluster / len(dated)) if dated else 0:6.1f}%")

    dst = os.path.join(OUT, "_coverage.json")
    with open(dst, "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote", dst)


if __name__ == "__main__":
    main()
