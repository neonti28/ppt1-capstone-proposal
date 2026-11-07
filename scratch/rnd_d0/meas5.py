"""RND-D0 measurement 5: discrete states, transitions, onsets, clean baseline length."""
import json, os, glob
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
BINS = f"{BASE}/scratch/v9_d1/bins"
DS = f"{BASE}/scratch/v9_d1/datasets"
OUT = os.path.dirname(os.path.abspath(__file__))
VIB_TH = 32.17405
res = {"bins_states": {}, "window_baseline": {}}


def episodes(mask, ts):
    """Return list of (start_idx, end_idx) runs of True."""
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - 1)); start = None
    if start is not None:
        out.append((start, len(mask) - 1))
    return out


def longest_zero_run(mask):
    best = cur = 0
    for v in mask:
        if not v:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


# ---------- A. states from bins ----------
for p in sorted(glob.glob(f"{BINS}/*.csv.gz")):
    w = os.path.basename(p).replace(".csv.gz", "")
    b = pd.read_csv(p, compression="gzip")
    ts = b["ts_bin"].to_numpy()
    n = len(b)
    d = {}
    def state(col, th):
        if col not in b.columns:
            return None
        v = b[col].to_numpy(dtype="float64")
        with np.errstate(invalid="ignore"):
            s = np.where(np.isnan(v), False, v >= th)
        return s
    states = {
        "STUCK": state("stuck_max", 1.0),
        "SHKRSK": state("shk_max", 1.0),
        "VIBLAT": state("vib_max", VIB_TH),
        "CRPM_present": (b["crpm_n"].to_numpy() > 0) if "crpm_n" in b.columns else None,
    }
    for nm, s in states.items():
        if s is None:
            d[nm] = {"available": False}
            continue
        eps = episodes(s, ts)
        edges = int(np.sum((~np.r_[True, s[:-1]]) & s)) if len(s) else 0
        durs = [ts[e] - ts[st] + 60 for st, e in eps]
        d[nm] = {
            "available": True,
            "minutes_in_state": int(s.sum()),
            "frac_minutes": float(s.mean()),
            "n_episodes": len(eps),
            "n_0to1_edges": edges,
            "n_state_changes": int(np.sum(s[1:] != s[:-1])) if len(s) > 1 else 0,
            "episode_median_min": float(np.median(durs) / 60) if durs else None,
            "episode_max_min": float(np.max(durs) / 60) if durs else None,
        }
    # combined clean baseline: minutes with no STUCK/SHK/VIB state
    comb = np.zeros(n, dtype=bool)
    for nm in ("STUCK", "SHKRSK", "VIBLAT"):
        s = states.get(nm)
        if s is not None:
            comb |= s
    d["clean_baseline_all_three"] = {
        "longest_clean_run_min": int(longest_zero_run(comb)),
        "frac_clean_minutes": float((~comb).mean()),
    }
    # channel availability (no-label channel candidates)
    chans = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM", "depth", "dbtm"]
    d["channel_presence"] = {c: float(b[f"{c}_mean"].notna().mean()) for c in chans if f"{c}_mean" in b.columns}
    res["bins_states"][w] = d
    print(f"[bins-state] {w}: STUCK eps={d['STUCK'].get('n_episodes')} SHK eps={d['SHKRSK'].get('n_episodes')} "
          f"VIB eps={d['VIBLAT'].get('n_episodes')} clean_min={d['clean_baseline_all_three']['longest_clean_run_min']}")

# ---------- B. baseline from window datasets (label == 0 runs, minute grid) ----------
LABEL = {"vib": "y_vib", "ssi": "y_ssi", "shk": "y_shk", "stuck_k1": "y_stuck",
         "stuck_k2": "y_stuck_onset", "hyd_ki": "y_hyd"}
for e, lab in LABEL.items():
    df = pd.read_csv(f"{DS}/{e}.csv.gz", compression="gzip", usecols=["well", "ts_bin", lab], low_memory=False)
    per = {}
    for w, g in df.groupby("well"):
        g = g.sort_values("ts_bin")
        ts = g["ts_bin"].to_numpy()
        y = g[lab].to_numpy()
        # split into contiguous minute segments (gap > 60 s starts new segment)
        seg_start = np.r_[True, np.diff(ts) > 60]
        seg_id = np.cumsum(seg_start)
        best = 0
        for sid in np.unique(seg_id):
            m = seg_id == sid
            best = max(best, longest_zero_run(y[m]))
        eps = episodes(y == 1, ts)
        dur = [(b_ - a_) + 1 for a_, b_ in eps]
        per[w] = {"n_rows": int(len(y)), "n_pos": int((y == 1).sum()),
                  "prev": float((y == 1).mean()),
                  "longest_clean_run_min": int(best),
                  "n_pos_segments_label1": len(eps),
                  "pos_segment_median_min": (float(np.median(dur)) if dur else None)}
    res["window_baseline"][e] = per
    print(f"[baseline] {e}: " + "; ".join(f"{w}:clean={v['longest_clean_run_min']}m,pos_seg={v['n_pos_segments_label1']}" for w, v in per.items()))

with open(f"{OUT}/meas5_states_baseline.json", "w") as fh:
    json.dump(res, fh, indent=1, default=str)
print("WROTE", f"{OUT}/meas5_states_baseline.json")
