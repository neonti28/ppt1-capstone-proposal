"""T_A: benar-benar mengukur laju sampel dan isi spektrum kanal getaran Volve.

Tujuan: uji pemisah untuk klaim 'VMD/EMD/wavelet tidak layak'.
Output: scratch/rnd_r3/out_t_a.json
Jalankan: .venv/bin/python test_a_sampling.py
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = Path(__file__).parent / "out_t_a.json"
WELLS = ["F-14", "F-15_S", "F-15A", "F-9", "F-5"]
CHAN = "VIBLAT_RT"

res = {"channel": CHAN, "wells": {}}

for w in WELLS:
    p = BASE / "data/volve/witsml_parsed" / f"{w}.csv"
    if not p.exists():
        res["wells"][w] = {"status": "file_missing"}
        continue
    try:
        df = pd.read_csv(p, usecols=["timestamp", CHAN], engine="c")
    except ValueError as e:
        res["wells"][w] = {"status": "channel_absent", "err": str(e)[:120]}
        continue
    df = df.dropna(subset=[CHAN])
    n_raw = int(len(df))
    if n_raw < 10:
        res["wells"][w] = {"status": "too_few", "n": n_raw}
        continue
    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.assign(_ts=ts).dropna(subset=["_ts"]).sort_values("_ts")
    t = df["_ts"].values.astype("datetime64[s]").astype(np.int64).astype(float)
    x = df[CHAN].to_numpy(dtype=float)
    dt = np.diff(t)
    dt_pos = dt[dt > 0]
    med_dt = float(np.median(dt_pos)) if dt_pos.size else float("nan")
    fs = 1.0 / med_dt if med_dt and med_dt > 0 else float("nan")

    # segmen kontinu terpanjang: tidak ada gap > 60 dtk
    brk = np.where(dt > 60)[0]
    if brk.size:
        segs = np.split(np.arange(len(x)), brk + 1)
        longest = max(segs, key=len)
    else:
        longest = np.arange(len(x))
    xseg = x[longest]
    dur = float(t[longest[-1]] - t[longest[0]]) if len(longest) > 1 else 0.0

    rec = {
        "status": "ok",
        "n_samples": n_raw,
        "median_dt_s": round(med_dt, 4),
        "fs_hz": round(fs, 6),
        "nyquist_hz": round(fs / 2.0, 6),
        "n_gap_gt_60s": int(brk.size),
        "longest_segment_samples": int(len(longest)),
        "longest_segment_hours": round(dur / 3600.0, 3),
        "value_min": round(float(np.nanmin(xseg)), 5),
        "value_max": round(float(np.nanmax(xseg)), 5),
        "value_std": round(float(np.nanstd(xseg)), 6),
    }

    # spektrum pada segmen kontinu terpanjang, di-resample seragam ke median dt
    if len(xseg) >= 64:
        tin = t[longest].astype(float)
        tu = np.arange(tin[0], tin[-1], med_dt)
        xu = np.interp(tu, tin, xseg)
        xu = xu - xu.mean()
        nfft = len(xu)
        win = np.hanning(nfft)
        spec = np.abs(np.fft.rfft(xu * win)) ** 2
        freqs = np.fft.rfftfreq(nfft, d=med_dt)
        tot = spec.sum()
        if tot > 0:
            dom = float(freqs[int(np.argmax(spec))])
            # fraksi daya di atas 0,05 Hz dan di atas 0,1 Hz
            f005 = float(spec[freqs > 0.05].sum() / tot)
            f010 = float(spec[freqs > 0.1].sum() / tot)
            # bandwidth efektif: frekuensi tempat kumulatif daya = 90%
            cum = np.cumsum(spec) / tot
            f90 = float(freqs[int(np.searchsorted(cum, 0.90))]) if cum[-1] >= 0.90 else float(freqs[-1])
            rec.update({
                "psd_n": int(nfft),
                "psd_dominant_hz": round(dom, 6),
                "psd_frac_power_gt_0p05hz": round(f005, 5),
                "psd_frac_power_gt_0p10hz": round(f010, 5),
                "psd_f90_hz": round(f90, 6),
            })
            # deteksi puncak pada pita di atas 0,1 Hz: apakah ada energi berarti
            hi = spec[freqs > 0.10]
            rec["psd_max_bin_gt_0p10hz_frac"] = round(float(hi.max() / tot), 8) if hi.size else 0.0
    res["wells"][w] = rec

OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
