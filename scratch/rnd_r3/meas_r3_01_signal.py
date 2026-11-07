#!/usr/bin/env python3
"""
RND-R3 / M1: inventaris sinyal untuk VMD/EMD/wavelet (versi hemat memori).
Membaca CSV WITSML mentah per potongan (chunksize) supaya tidak menghabiskan RAM.

Untuk tiap kanal:
  n sampel, dt median (dtk), laju (Hz), Nyquist (Hz), jumlah segmen kontinu,
  segmen terpanjang (sampel + jam), jumlah jendela komplit untuk 256/512/1024,
  spektrum segmen terpanjang (frekuensi dominan, resolusi frekuensi, fraksi daya).
Output: m1_signal_inventory.json
"""
import json, os, sys
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
RAW = os.path.join(BASE, "data/volve/witsml_parsed")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "m1_signal_inventory.json")

TARGETS = {
    "F-10":   ["SHKRSK_RT", "CRPM_RT", "TQA"],
    "F-12":   ["CRPM_RT", "SHKRSK_RT"],
    "F-14":   ["VIBLAT_RT", "SHKRSK_RT", "CRPM_RT"],
    "F-15A":  ["VIBLAT_RT", "CRPM_RT", "SHKRSK_RT"],
    "F-15_S": ["VIBLAT_RT", "CRPM_RT", "SHKRSK_RT"],
    "F-5":    ["VIBLAT_RT", "CRPM_RT", "SHKRSK_RT"],
    "F-7":    ["SHKRSK_RT"],
    "F-9":    ["VIBLAT_RT", "STUCK_RT"],
    "F-9_A":  ["SHKRSK_RT", "STUCK_RT"],
}
WINDOW_CANDIDATES = [256, 512, 1024]
GAP_SEC = 60.0
CHUNK = 60000


def contiguous_segments(ts, gap=GAP_SEC):
    if len(ts) < 2:
        return [(0, len(ts))] if len(ts) else []
    d = np.diff(ts)
    cuts = np.where(d > gap)[0]
    segs, start = [], 0
    for c in cuts:
        segs.append((start, c + 1))
        start = c + 1
    segs.append((start, len(ts)))
    return segs


def spectral(y, dt):
    y = np.asarray(y, dtype=float)
    y = y[np.isfinite(y)]
    n = len(y)
    if n < 32 or dt <= 0:
        return None
    ym = y - y.mean()
    fs = 1.0 / dt
    spec = np.abs(np.fft.rfft(ym * np.hanning(n))) ** 2
    freqs = np.fft.rfftfreq(n, d=dt)
    spec[0] = 0.0
    tot = spec.sum()
    if tot <= 0:
        return None
    k = int(np.argmax(spec))
    nyq = fs / 2.0
    return {
        "n_fft": int(n), "fs_hz": float(fs), "nyquist_hz": float(nyq),
        "freq_resolution_hz": float(fs / n),
        "dominant_freq_hz": float(freqs[k]),
        "dominant_period_s": float(1.0 / freqs[k]) if freqs[k] > 0 else None,
        "frac_power_below_half_nyquist": float(spec[(freqs > 0) & (freqs <= nyq / 2)].sum() / tot),
        "frac_power_below_0p01hz": float(spec[(freqs > 0) & (freqs < 0.01)].sum() / tot),
        "n_bins_0_to_1hz": int(((freqs > 0) & (freqs < 1.0)).sum()),
        "peak_spectral_share": float(spec[k] / tot),
    }


def process_well(well, chans):
    path = os.path.join(RAW, well + ".csv")
    if not os.path.exists(path):
        return [{"well": well, "status": "FILE TIDAK ADA"}]
    head = pd.read_csv(path, nrows=0)
    have = [c for c in chans if c in head.columns]
    missing = [c for c in chans if c not in head.columns]
    out = [{"well": well, "channel": c, "status": "KANAL TIDAK ADA"} for c in missing]
    if not have:
        return out
    acc = {c: ([], []) for c in have}   # ts_int_sec, value
    for chunk in pd.read_csv(path, usecols=["timestamp"] + have, chunksize=CHUNK,
                             dtype={"timestamp": "string"}, low_memory=False):
        t = pd.to_datetime(chunk["timestamp"], errors="coerce", utc=True, format="ISO8601")
        ti = pd.Series(t.dt.tz_localize(None).astype("int64") // 10**9, index=chunk.index)
        for c in have:
            v = pd.to_numeric(chunk[c], errors="coerce")
            m = v.notna() & t.notna()
            if m.any():
                acc[c][0].append(ti[m].to_numpy(dtype=np.int64))
                acc[c][1].append(v[m].to_numpy(dtype=float))
        del chunk, t, ti
    for c in have:
        if not acc[c][1]:
            out.append({"well": well, "channel": c, "status": "TIDAK ADA NILAI NUMERIK"})
            continue
        ts_raw = np.concatenate(acc[c][0]).astype(np.int64)
        y_raw = np.concatenate(acc[c][1])
        n_rows = int(len(ts_raw))
        # KOREKSI PENTING: berkas terparse memuat beberapa baris per timestamp
        # (satu baris per kanal/rekaman). diff mentah menghasilkan cadence palsu 1 Hz.
        # Dedup: satu nilai per timestamp (rata-rata bila ada duplikat).
        ser = pd.Series(y_raw, index=ts_raw)
        ser = ser.groupby(level=0).mean()
        ts = ser.index.to_numpy().astype(float)
        y = ser.to_numpy(dtype=float)
        order = np.argsort(ts, kind="stable")
        ts, y = ts[order], y[order]
        dt = np.diff(ts)
        dt = dt[dt > 0]
        dt_med = float(np.median(dt)) if len(dt) else 0.0
        segs = contiguous_segments(ts)
        L = max(e - s for s, e in segs)
        longest = max(segs, key=lambda s: s[1] - s[0])
        wc = {}
        for w in WINDOW_CANDIDATES:
            wc[str(w)] = {"total": int(sum((e - s) // w for s, e in segs)),
                          "di_segmen_terpanjang": int(L // w)}
        out.append({
            "well": well, "channel": c, "status": "ADA",
            "n_baris_mentah": n_rows, "n_sampel": int(len(y)), "dt_median_s": dt_med,
            "laju_hz": (1.0 / dt_med) if dt_med > 0 else None,
            "nyquist_hz": (0.5 / dt_med) if dt_med > 0 else None,
            "n_segmen_kontinu": int(len(segs)),
            "segmen_terpanjang_sampel": int(L),
            "segmen_terpanjang_jam": float(L * dt_med / 3600.0),
            "gap_gt_60s": int((dt > GAP_SEC).sum()),
            "jendela": wc,
            "spektral": spectral(y[longest[0]:longest[1]], dt_med),
        })
    return out


def main():
    res = {"generated_at": pd.Timestamp.now().isoformat(timespec="seconds"),
           "sumber": "data/volve/witsml_parsed/<WELL>.csv", "gap_breaker_sec": GAP_SEC,
           "window_candidates": WINDOW_CANDIDATES, "channels": []}
    for well, chans in TARGETS.items():
        print("..", well, flush=True)
        res["channels"].extend(process_well(well, chans))
        with open(OUT, "w") as f:
            json.dump(res, f, indent=2)
    for e in res["channels"]:
        if e.get("status") != "ADA":
            print(f'{e["well"]:7s} {e.get("channel",""):10s} {e["status"]}')
        else:
            sp = e["spektral"] or {}
            print(f'{e["well"]:7s} {e["channel"]:10s} n={e["n_sampel"]:7d} '
                  f'fs={e["laju_hz"]:.4f} nyq={e["nyquist_hz"]:.4f} '
                  f'Lmax={e["segmen_terpanjang_sampel"]:6d} '
                  f'w1024={e["jendela"]["1024"]["total"]:4d} '
                  f'fdom={sp.get("dominant_freq_hz", float("nan")):.5f}Hz '
                  f'pk={sp.get("peak_spectral_share", float("nan")):.3f}')
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
