#!/usr/bin/env python3
"""
20_join_md_time.py — Uji hipotesis: baris USROP (depth-indexed, tanpa tanggal) bisa diberi
timestamp via interpolasi linear md->waktu per wellbore dari DDR Volve.

READ-ONLY terhadap input (data/USROP_labeled.csv, data/volve/ddr.parquet).
Output:
  data/volve/usrop_timestamped.csv   = USROP_labeled.csv + est_timestamp (ISO UTC) + join_status
  docs/V2_DATA_JOIN_METRICS.json     = metriks coverage per wellbore (dipakai laporan)

Sumber pasangan (md, waktu) per wellbore DDR (SEMUA aktivitas, bukan hanya event):
  1. activity[]      : md  + dTimStart
  2. statusInfo[]    : md  + dTim   (laporan harian)
  3. surveyStation[] : md  + dTim   (stasiun survei)
Filter: md > 0 (membuang sentinel -999.99), waktu valid & tahun >= 1990 (membuang 1980-01-01).

Rumus interpolasi (per wellbore):
  anchor diurutkan menaik per md, duplikat md dibuang (simpan waktu PALING AWAL =
  waktu pertama kedalaman itu tercapai).
  Untuk baris USROP dengan md = x:
    jika x < md_min atau x > md_max  -> NaT, join_status = 'out_of_range'
    selainnya, cari jarak md terdekat [md_j, md_{j+1}] dengan md_j <= x <= md_{j+1}:
      t(x) = t_j + (x - md_j) * (t_{j+1} - t_j) / (md_{j+1} - md_j)
      -> est_timestamp, join_status = 'interpolated'
  Baris tanpa pemetaan wellbore -> NaT, join_status = 'no_wellbore_match'.
"""
import json
import os
from collections import defaultdict

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DDR_PATH = os.path.join(ROOT, "data", "volve", "ddr.parquet")
USROP_PATH = os.path.join(ROOT, "data", "USROP_labeled.csv")
OUT_CSV = os.path.join(ROOT, "data", "volve", "usrop_timestamped.csv")
OUT_METRICS = os.path.join(ROOT, "docs", "V2_DATA_JOIN_METRICS.json")

# Pemetaan kolom `well` (nama file Norway) -> nameWellbore di DDR.
# Dasar bukti (lihat docs/V2_DATA_JOIN_REPORT.md bagian Pemetaan Wellbore):
#   * 5 well (F-9 A, F-7, F-14, F-5, F-9) cocok by name + signature ukuran lubang.
#   * USROP 'F-15' hanya punya pass 17.5in + 8.5in; di keluarga F-15 hanya
#     'NO 15/9-F-15 A' yang menggali 17.5in (casing 13-3/8") tanpa pass 12.25in -> A.
#   * USROP 'F-15S' (pass 12.25in + 8.5in, md_max 4090.001) tidak punya nama sama di DDR;
#     satu-satunya wellbore DDR dengan signature {12.25, 8.5} + TD 4090 adalah
#     'NO 15/9-F-15' (casing 9-5/8" di lubang 12.25in) -> main.
WELL_MAP = {
    "USROP_A 0 N-NA_F-9_Ad.csv": "NO 15/9-F-9 A",
    "USROP_A 1 N-S_F-7d.csv": "NO 15/9-F-7",
    "USROP_A 2 N-SH_F-14d.csv": "NO 15/9-F-14",
    "USROP_A 3 N-SH-F-15d.csv": "NO 15/9-F-15 A",
    "USROP_A 4 N-SH_F-15Sd.csv": "NO 15/9-F-15",
    "USROP_A 5 N-SH-F-5d.csv": "NO 15/9-F-5",
    "USROP_A 6 N-SH_F-9d.csv": "NO 15/9-F-9",
}

MIN_YEAR = 1990  # di bawah ini dianggap sentinel (dTim default 1980-01-01)


def parse_ts(value):
    """-> epoch detik UTC (float) atau None bila tidak valid / sentinel."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    ts = pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(ts):
        return None
    if ts.year < MIN_YEAR:
        return None
    return ts.timestamp()


def parse_md(value):
    try:
        md = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(md) or md <= 0:
        return None
    return md


def collect_pairs(ddr):
    """Kumpulkan pasangan (md, epoch) dari activity + statusInfo + surveyStation per wellbore."""
    pairs = defaultdict(list)          # wellbore -> [(md, epoch, sumber)]
    src_count = defaultdict(lambda: defaultdict(int))
    n_drop_md = n_drop_ts = 0
    for _, row in ddr.iterrows():
        wb = row["nameWellbore"]

        for it in (row["activity"] if isinstance(row["activity"], np.ndarray) else []):
            if not isinstance(it, dict):
                continue
            md = parse_md(it.get("md"))
            if md is None:
                n_drop_md += 1
                continue
            ep = parse_ts(it.get("dTimStart"))
            if ep is None:
                n_drop_ts += 1
                continue
            pairs[wb].append((md, ep, "activity"))
            src_count[wb]["activity"] += 1

        st = row["statusInfo"]
        if isinstance(st, np.ndarray):
            for it in st:
                if not isinstance(it, dict):
                    continue
                md = parse_md(it.get("md"))
                ep = parse_ts(it.get("dTim")) if md is not None else None
                if md is None or ep is None:
                    continue
                pairs[wb].append((md, ep, "statusInfo"))
                src_count[wb]["statusInfo"] += 1

        ss = row["surveyStation"]
        if isinstance(ss, np.ndarray):
            for it in ss:
                if not isinstance(it, dict):
                    continue
                md = parse_md(it.get("md"))
                ep = parse_ts(it.get("dTim")) if md is not None else None
                if md is None or ep is None:
                    continue
                pairs[wb].append((md, ep, "surveyStation"))
                src_count[wb]["surveyStation"] += 1

    return pairs, src_count, n_drop_md, n_drop_ts


def build_anchor_curve(pairs):
    """Jendela kampanye + dedupe md (simpan waktu paling awal) + sort menaik.

    Jendela kampanye: [waktu terawal, waktu pertama wellbore mencapai md maksimum].
    Tujuan: aktivitas kempanye lanjutan (workover/P&A bertahun-tahun kemudian) tidak
    mencemari kurva drilling md->waktu.
    """
    if not pairs:
        return None, None
    md_all = np.array([p[0] for p in pairs])
    t_all = np.array([p[1] for p in pairs])
    t_first = float(t_all.min())
    md_max = float(md_all.max())
    t_td = float(t_all[md_all >= md_max].min())

    keep = [(m, t) for m, t, _ in pairs if t_first <= t <= t_td]
    if not keep:
        return None, None

    best = {}
    for md, t in keep:
        if md not in best or t < best[md]:
            best[md] = t
    mds = np.array(sorted(best), dtype=float)
    tss = np.array([best[m] for m in mds], dtype=float)
    return mds, tss


def interpolate(mds, tss, x):
    """Interpolasi linear; di luar jangkauan -> np.nan."""
    if x < mds[0] or x > mds[-1]:
        return np.nan
    return float(np.interp(x, mds, tss))


def main():
    ddr = pd.read_parquet(DDR_PATH)
    pairs, src_count, n_drop_md, n_drop_ts = collect_pairs(ddr)

    print(f"DDR rows={len(ddr)}; pasangan terkumpul per wellbore (setelah filter md>0 & tahun>=1990):")
    for wb in sorted(pairs):
        print(f"  {wb:>16}: {len(pairs[wb]):5d}  {dict(src_count[wb])}")
    print(f"drop md tidak valid: {n_drop_md}; drop waktu tidak valid/sentinel: {n_drop_ts}")

    curves = {}
    curve_stats = {}
    for wb, prs in pairs.items():
        mds, tss = build_anchor_curve(prs)
        if mds is None or len(mds) < 2:
            continue
        curves[wb] = (mds, tss)
        gap = np.diff(mds)
        neg = int((np.diff(tss) < 0).sum())
        curve_stats[wb] = dict(
            n_pairs_all=len(prs),
            n_anchor=int(len(mds)),
            md_min=float(mds[0]), md_max=float(mds[-1]),
            gap_median=float(np.median(gap)),
            gap_p95=float(np.percentile(gap, 95)),
            gap_max=float(gap.max()),
            n_negative_slope=neg,
            share_negative_slope=round(neg / len(gap), 4),
            t_first=pd.Timestamp(tss[0], unit="s", tz="UTC").isoformat(),
            t_last=pd.Timestamp(tss[-1], unit="s", tz="UTC").isoformat(),
        )

    usrop = pd.read_csv(USROP_PATH)
    n_in = len(usrop)
    unknown = sorted(set(usrop["well"].dropna().unique()) - set(WELL_MAP))
    if unknown:
        print(f"PERINGATAN: nilai well tanpa pemetaan: {unknown}")

    md_vals = pd.to_numeric(usrop["Measured Depth m"], errors="coerce").to_numpy(dtype=float)
    est = np.full(n_in, np.nan)
    status = np.array(["no_wellbore_match"] * n_in, dtype=object)
    matched_wb = np.array([""] * n_in, dtype=object)

    for well_name, wb in WELL_MAP.items():
        mask = (usrop["well"] == well_name).to_numpy()
        if not mask.any():
            print(f"PERINGATAN: well '{well_name}' tidak ada di USROP_labeled.csv")
            continue
        matched_wb[mask] = wb
        if wb not in curves:
            status[mask] = "no_wellbore_match"
            continue
        mds, tss = curves[wb]
        for i in np.flatnonzero(mask):
            x = md_vals[i]
            if not np.isfinite(x):
                status[i] = "out_of_range"
                continue
            t = interpolate(mds, tss, x)
            if np.isnan(t):
                status[i] = "out_of_range"
            else:
                est[i] = t
                status[i] = "interpolated"

    # ---- kualitas per wellbore: inversi waktu di output & sensitivitas estimator ----
    # inversi = baris USROP berurutan (md menaik) tetapi est_timestamp mundur ke belakang
    # first-reach = estimator pembanding: T(x) = min{t_i : md_i >= x} (monoton naik)
    qual = {}
    for well_name, wb in WELL_MAP.items():
        mask = (usrop["well"] == well_name).to_numpy()
        if wb not in curves:
            continue
        mds, tss = curves[wb]
        suf_min = np.minimum.accumulate(tss[::-1])[::-1]  # min ke kanan (untuk first-reach)

        idx = np.flatnonzero(mask)
        order = idx[np.argsort(md_vals[idx], kind="stable")]
        x = md_vals[order]
        t = est[order]
        ok = ~np.isnan(t)
        step_days = np.diff(t[ok]) / 86400.0
        n_back = int((step_days < 0).sum())
        back = -step_days[step_days < 0]

        xi = x[ok]
        pos = np.searchsorted(mds, xi, side="left")
        t_fr = suf_min[pos]
        delta_days = np.abs(t[ok] - t_fr) / 86400.0

        # lebar bracket interpolasi (t_{j+1} - t_j) untuk tiap baris = batas kasar error
        j = np.searchsorted(mds, xi, side="right") - 1
        j = np.clip(j, 0, len(mds) - 2)
        bracket = np.abs(tss[j + 1] - tss[j]) / 86400.0  # lebar absolut

        qual[well_name] = dict(
            n_rows_time=int(ok.sum()),
            n_backstep=n_back,
            share_backstep=round(n_back / max(len(step_days), 1), 4),
            backstep_median_days=round(float(np.median(back)), 3) if len(back) else 0.0,
            backstep_p95_days=round(float(np.percentile(back, 95)), 3) if len(back) else 0.0,
            backstep_max_days=round(float(back.max()), 3) if len(back) else 0.0,
            bracket_median_days=round(float(np.median(bracket)), 3),
            bracket_p95_days=round(float(np.percentile(bracket, 95)), 3),
            bracket_max_days=round(float(bracket.max()), 3),
            sens_median_days=round(float(np.median(delta_days)), 3),
            sens_p95_days=round(float(np.percentile(delta_days, 95)), 3),
        )

    # presisi detik (akurasi sebenarnya jauh lebih kasar - lihat laporan)
    est_iso = ["" if np.isnan(t) else
               pd.Timestamp(int(round(t)), unit="s", tz="UTC").isoformat().replace("+00:00", "Z")
               for t in est]

    out = usrop.copy()
    out["est_timestamp"] = est_iso
    out["join_status"] = status
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    # ---- metriks coverage per wellbore ----
    rows = []
    for well_name, wb in WELL_MAP.items():
        mask = (usrop["well"] == well_name).to_numpy()
        n = int(mask.sum())
        st = status[mask]
        x = md_vals[mask]
        n_int = int((st == "interpolated").sum())
        n_oor = int((st == "out_of_range").sum())
        n_nom = int((st == "no_wellbore_match").sum())
        valid = x[np.isfinite(x)]
        cs = curve_stats.get(wb, {})
        t_ok = est[mask & ~np.isnan(est)]
        rows.append(dict(
            usrop_well=well_name,
            ddr_wellbore=wb,
            n_rows=n,
            n_interpolated=n_int,
            n_out_of_range=n_oor,
            n_no_wellbore_match=n_nom,
            coverage_pct=round(100.0 * n_int / n, 3) if n else 0.0,
            usrop_md_min=float(valid.min()) if len(valid) else None,
            usrop_md_max=float(valid.max()) if len(valid) else None,
            anchor_md_min=cs.get("md_min"),
            anchor_md_max=cs.get("md_max"),
            n_anchor=cs.get("n_anchor"),
            gap_median_m=cs.get("gap_median"),
            gap_p95_m=cs.get("gap_p95"),
            gap_max_m=cs.get("gap_max"),
            share_negative_slope=cs.get("share_negative_slope"),
            est_t_min=pd.Timestamp(t_ok.min(), unit="s", tz="UTC").isoformat() if len(t_ok) else None,
            est_t_max=pd.Timestamp(t_ok.max(), unit="s", tz="UTC").isoformat() if len(t_ok) else None,
        ))

    total = dict(
        n_rows=int(n_in),
        n_interpolated=int((status == "interpolated").sum()),
        n_out_of_range=int((status == "out_of_range").sum()),
        n_no_wellbore_match=int((status == "no_wellbore_match").sum()),
        coverage_pct=round(100.0 * (status == "interpolated").sum() / n_in, 3),
        n_md_nan=int((~np.isfinite(md_vals)).sum()),
        dropped_md=n_drop_md,
        dropped_time=n_drop_ts,
    )

    metrics = dict(per_well=rows, quality=qual, total=total)
    os.makedirs(os.path.dirname(OUT_METRICS), exist_ok=True)
    with open(OUT_METRICS, "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2, ensure_ascii=False)

    print("\n=== COVERAGE PER WELLBORE ===")
    for r in rows:
        print(f"  {r['usrop_well']:<28} -> {r['ddr_wellbore']:<16} "
              f"rows={r['n_rows']:6d} interp={r['n_interpolated']:6d} "
              f"oor={r['n_out_of_range']:5d} nomatch={r['n_no_wellbore_match']:4d} "
              f"cov={r['coverage_pct']:6.2f}%  md[{r['usrop_md_min']:.1f},{r['usrop_md_max']:.1f}] "
              f"anchor[{r['anchor_md_min']:.1f},{r['anchor_md_max']:.1f}] n={r['n_anchor']} "
              f"gap_med={r['gap_median_m']:.3f}m negSlope={r['share_negative_slope']}")
    print("\n=== KUALITAS: inversi waktu & sensitivitas estimator (hari) ===")
    for well_name, q in qual.items():
        print(f"  {well_name:<28} backstep={q['n_backstep']:5d}/{q['n_rows_time'] - 1:<5d} "
              f"({q['share_backstep'] * 100:5.1f}%) median={q['backstep_median_days']:8.3f} "
              f"p95={q['backstep_p95_days']:9.3f} max={q['backstep_max_days']:10.3f} | "
              f"sens_median={q['sens_median_days']:.3f} sens_p95={q['sens_p95_days']:.3f} | "
              f"bracket med={q['bracket_median_days']:.3f}d p95={q['bracket_p95_days']:.3f}d "
              f"max={q['bracket_max_days']:.1f}d")
    print("\n=== TOTAL ===")
    print(json.dumps(total, indent=2))
    print(f"\nOutput: {OUT_CSV}")
    print(f"Metrics: {OUT_METRICS}")


if __name__ == "__main__":
    main()
